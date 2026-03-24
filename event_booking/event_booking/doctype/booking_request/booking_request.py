import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff


class BookingRequest(Document):
	def validate(self):
		self.check_venue_availability()

		if not self.is_new():
			if self.status == "Draft" and self.rejection_reason:
				self.rejection_reason = None

	def before_save(self):
		self.calculate_amounts()
		self.calculate_payments()
		self.update_status()

	def calculate_amounts(self):
		days = 0
		if self.event_from_date and self.event_to_date:
			days = max(0, date_diff(self.event_to_date, self.event_from_date) + 1)

		venue_rate = frappe.db.get_value("Venue", self.venue, "daily_rate") if self.venue else 0
		venue_rate = venue_rate or 0

		package_price = (
			frappe.db.get_value("Event Package", self.event_package, "total_price")
			if self.event_package
			else 0
		)
		package_price = package_price or 0

		self.estimated_cost = (venue_rate * days) + package_price

		discount = self.discount or 0

		tax_rate = frappe.db.get_single_value("Event Booking Settings", "default_tax_percentage") or 0

		tax_rate = tax_rate / 100

		taxable_amount = max(0, self.estimated_cost - discount)

		self.tax_amount = taxable_amount * tax_rate
		self.total_amount = taxable_amount + self.tax_amount

	def calculate_payments(self):
		total_paid = 0

		for row in self.payments:
			total_paid += row.amount or 0

		self.total_paid = total_paid
		self.balance_due = (self.total_amount or 0) - total_paid

		if self.total_paid > (self.total_amount or 0):
			frappe.throw(_("Total Paid cannot exceed Total Amount"))

	def update_status(self):
		if self.balance_due == 0 and self.total_amount > 0:
			self.status = "Completed"

	def check_venue_availability(self):
		if not self.venue or not self.event_from_date or not self.event_to_date:
			return

		clashes = frappe.db.sql(
			"""
            SELECT name FROM `tabBooking Request`
            WHERE venue = %s
            AND status IN ('Pending Approval','Approved','Completed')
            AND name != %s
            AND NOT (
                event_to_date < %s OR event_from_date > %s
            )
        """,
			(self.venue, self.name, self.event_from_date, self.event_to_date),
		)

		if clashes:
			frappe.throw(_("Venue already booked for the selected dates."))


def get_permission_query_conditions(user):
	if not user:
		user = frappe.session.user

	roles = frappe.get_roles(user)

	if "Booking Admin" in roles:
		return ""

	if "Front Desk" in roles:
		return f"`tabBooking Request`.assigned_front_desk = '{user}'"

	return ""
