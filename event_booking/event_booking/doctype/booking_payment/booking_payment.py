import frappe
from frappe.model.document import Document

class BookingPayment(Document):

    def on_submit(self):
        self.update_booking_totals()

    # def on_cancel(self):
    #     self.update_booking_totals(self.booking)


    def update_booking_totals(self):
        booking = frappe.get_doc("Booking Request", self.booking)
        settled=self.paid_amount+booking.settled_amount
        booking.settled_amount=settled
        if booking.final_amount==settled:
            booking.progress = "Paid"
        elif settled > 0:
            booking.progress = "Partially Paid"
        else:
            booking.progress = "Unpaid"
        booking.save()