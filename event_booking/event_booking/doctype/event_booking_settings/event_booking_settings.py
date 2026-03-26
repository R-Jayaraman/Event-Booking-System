import frappe
from frappe.model.document import Document


class EventBookingSettings(Document):

    def validate(self):
        if self.tax_percentage is not None:
            if self.tax_percentage < 0 or self.tax_percentage > 100:
                frappe.throw("Tax must be between 0 and 100")