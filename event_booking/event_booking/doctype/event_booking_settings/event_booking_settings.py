import frappe
from frappe.model.document import Document

class EventBookingSettings(Document):

    def validate(self):
        if self.default_tax is not None:
            if self.default_tax < 0 or self.default_tax > 100:
                frappe.throw("Tax must be between 0 and 100")