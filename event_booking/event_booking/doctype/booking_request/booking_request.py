import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, date_diff, today

class BookingRequest(Document):

    def validate(self):
        self.validate_dates()
        self.validate_category()
        self.validate_venue_availability()
        self.validate_max_booking_days()
        self.validate_capacity()
        self.validate_rejection()
        self.calculate_costs()
        self.calculate_payments_summary()

    def on_cancel(self):
        self.validate_cancellation()

    def validate_dates(self):
        if self.from_date and self.to_date:
            if getdate(self.from_date) > getdate(self.to_date):
                frappe.throw("From Date cannot be after To Date")

    def validate_category(self):
        if self.event_category:
            is_group = frappe.db.get_value(
                "Event Category",
                self.event_category,
                "is_group"
            )
            if is_group:
                frappe.throw("Please select a specific event type (not parent category)")

    def get_child_venues(self):
        venue = frappe.get_doc("Venue", self.venue)

        return frappe.get_all(
            "Venue",
            filters={
                "lft": [">=", venue.lft],
                "rgt": ["<=", venue.rgt],
                "is_group": 0
            },
            pluck="name"
        )

    def validate_venue_availability(self):
        if not (self.venue and self.from_date and self.to_date):
            return

        from_date = getdate(self.from_date)
        to_date = getdate(self.to_date)

        venue_doc = frappe.get_doc("Venue", self.venue)
        venues = self.get_child_venues() if venue_doc.is_group else [self.venue]

        for v in venues:
            conflict = frappe.db.exists("Booking Request", {
                "venue": v,
                "docstatus": ["!=", 2],
                "name": ["!=", self.name],
                "from_date": ["<=", to_date],
                "to_date": [">=", from_date]
            })

            if conflict:
                frappe.throw(f"Venue '{v}' is already booked for the selected dates")

    def validate_max_booking_days(self):
        if not self.from_date:
            return

        settings = frappe.get_single("Event Booking Settings")
        max_days = settings.max_advance_booking_days or 0

        booking_days = date_diff(getdate(self.from_date), getdate(today()))

        if booking_days < 0:
            frappe.throw("Booking date cannot be in the past")

        if max_days and booking_days > max_days:
            frappe.throw(f"Booking cannot be made more than {max_days} days in advance")

    def validate_capacity(self):
        if not (self.venue and self.guest_count):
            return

        venue_doc = frappe.get_doc("Venue", self.venue)

        if venue_doc.is_group:
            venues = self.get_child_venues()
            total_capacity = sum(
                frappe.db.get_value("Venue", v, "capacity") or 0
                for v in venues
            )
        else:
            total_capacity = frappe.db.get_value(
                "Venue",
                self.venue,
                "capacity"
            ) or 0

        if self.guest_count > total_capacity:
            frappe.throw("Guest count exceeds total venue capacity")

    def validate_rejection(self):
        if self.status == "Rejected" and not self.rejection_reason:
            frappe.throw("Rejection reason is mandatory")

    def validate_cancellation(self):
        if self.status == "Cancelled" and not self.cancellation_charges:
            frappe.throw("Cancellation charges must be entered")


    def calculate_costs(self):

        venue_cost = 0
        package_cost = 0

        if self.venue and self.from_date and self.to_date:
            venue_doc = frappe.get_doc("Venue", self.venue)
            venues = self.get_child_venues() if venue_doc.is_group else [self.venue]

            from_date = getdate(self.from_date)
            to_date = getdate(self.to_date)
            days = (to_date - from_date).days + 1

            for v in venues:
                rate = frappe.db.get_value("Venue", v, "daily_rate") or 0
                venue_cost += flt(rate) * days

        if self.event_package:
            package_cost = frappe.db.get_value(
                "Event Package",
                self.event_package,
                "total_price"
            ) or 0

        self.venue_cost = venue_cost
        self.package_cost = package_cost

        subtotal = venue_cost + package_cost

        profit_margin = self.profit_margin or 0
        profit_amount = subtotal * (profit_margin / 100)

        self.profit_amount = profit_amount

        settings = frappe.get_single("Event Booking Settings")
        tax_percent = settings.default_tax or 0

        tax_amount = subtotal * (tax_percent / 100)
        self.tax_amount = tax_amount

        total_amount = subtotal + profit_amount + tax_amount
        self.total_amount = total_amount

        discount = self.discount or 0
        final_amount = total_amount - discount
        self.final_amount = final_amount

    def calculate_payments_summary(self):
        total_paid = sum(flt(p.amount) for p in self.payments)

        self.total_paid = total_paid
        self.balance_amount = self.final_amount - total_paid


@frappe.whitelist()
def get_package_services(package):
    items = frappe.get_all(
        "Event Package Item",
        filters={"parent": package},
        fields=["service_provider", "amount"]
    )

    result = []
    for item in items:
        provider_type = frappe.db.get_value(
            "Service Provider",
            item.service_provider,
            "provider_type"
        )

        result.append({
            "service_provider": item.service_provider,
            "service_type": provider_type,
            "cost": item.amount
        })

    return result