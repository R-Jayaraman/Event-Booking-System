import frappe
from frappe.model.document import Document
from frappe.utils import flt


class EventPackage(Document):

    def validate(self):
        self.validate_dates()
        self.calculate_total()

    def validate_dates(self):
        if self.valid_from and self.valid_to:
            if self.valid_to < self.valid_from:
                frappe.throw("Valid To date must be after Valid From")

    def calculate_total(self):
        self.total_price = sum(flt(item.amount) for item in self.services)