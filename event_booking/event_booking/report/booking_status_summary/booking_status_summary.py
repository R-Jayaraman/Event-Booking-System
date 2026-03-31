import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count


def execute(filters=None):
    Booking = DocType("Booking Request")

    data = (
        frappe.qb.from_(Booking)
        .select(
            Booking.status,
            Count(Booking.name).as_("total_bookings")
        )
        .groupby(Booking.status)
    ).run(as_dict=True)

    columns = [
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Total Bookings",
            "fieldname": "total_bookings",
            "fieldtype": "Int",
            "width": 150
        }
    ]

    return columns, data