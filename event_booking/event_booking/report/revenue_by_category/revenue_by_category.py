import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):
    Booking = DocType("Booking Request")

    data = (
        frappe.qb.from_(Booking)
        .select(
            Booking.event_category,
            Sum(Booking.final_amount).as_("total_revenue")
        )
        .where(
            (Booking.docstatus == 1) &
            (Booking.event_category.isnotnull()) &
            (Booking.final_amount > 0)
        )
        .groupby(Booking.event_category)
    ).run(as_dict=True)

    columns = [
        {
            "label": "Event Category",
            "fieldname": "event_category",
            "fieldtype": "Link",
            "options": "Event Category",
            "width": 200
        },
        {
            "label": "Total Revenue",
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    return columns, data