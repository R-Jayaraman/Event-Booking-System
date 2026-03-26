import frappe
from frappe.model.document import Document

class Venue(Document):

    def validate(self):
        if self.is_group:
            self.calculate_group_values()


    def calculate_group_values(self):
        children = frappe.get_all(
            "Venue",
            filters={
                "parent_venue": self.name,
                "is_group": 0
            },
            fields=["name", "capacity", "daily_rate"]
        )

        total_capacity = 0
        total_rate = 0
        amenities_set = set()

        for c in children:
            total_capacity += c.capacity or 0
            total_rate += c.daily_rate or 0

            amenities = frappe.get_all(
                "Amenities",
                filters={"parent": c.name},
                fields=["amenity_name"]
            )

            for a in amenities:
                amenities_set.add(a.amenity_name)

        self.capacity = total_capacity
        self.daily_rate = total_rate

        self.set("amenities", [])

        for amenity in amenities_set:
            self.append("amenities", {
                "amenity_name": amenity
            })