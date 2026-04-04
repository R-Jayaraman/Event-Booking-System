import frappe
from frappe.model.document import Document
from frappe.utils import today

class BookingPayment(Document):
    # def validate(self):
    #     if not self.payment_date:
    #         self.payment_date = today()

    def on_submit(self):
        self.update_booking_totals()

    # def on_cancel(self):
    #     self.update_booking_totals(self.booking)


    def update_booking_totals(self):

    # get current settled amount directly
        current_settled = frappe.db.get_value(
            "Booking Request",
            self.booking,
            "settled_amount"
        ) or 0

        new_settled = current_settled + self.paid_amount

        # update settled amount
        frappe.db.set_value(
            "Booking Request",
            self.booking,
            "settled_amount",
            new_settled
        )

        # get final amount
        final_amount = frappe.db.get_value(
            "Booking Request",
            self.booking,
            "final_amount"
        ) or 0

        # decide progress
        if new_settled >= final_amount:
            progress = "Paid"
        elif new_settled > 0:
            progress = "Partially Paid"
        else:
            progress = "Unpaid"

        # update progress
        frappe.db.set_value(
            "Booking Request",
            self.booking,
            "progress",
            progress
        )