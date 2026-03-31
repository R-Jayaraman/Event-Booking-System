import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):

    Booking = DocType("Booking Request")
    Payment = DocType("Booking Payment")  # child table

    data = (
        frappe.qb.from_(Booking)
        .left_join(Payment)
        .on(Payment.parent == Booking.name)
        .select(
            Booking.venue,
            Sum(Booking.final_amount).as_("total_revenue"),
            Sum(Payment.amount).as_("total_paid")
        )
        .where(
            (Booking.docstatus == 1) &
            (Booking.venue.isnotnull())
        )
        .groupby(Booking.venue)
    ).run(as_dict=True)

    for row in data:
        total_paid = row.get("total_paid") or 0
        total_revenue = row.get("total_revenue") or 0
        row["balance"] = total_revenue - total_paid

    columns = [
        {
            "label": "Venue",
            "fieldname": "venue",
            "fieldtype": "Link",
            "options": "Venue",
            "width": 200
        },
        {
            "label": "Total Revenue",
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Total Paid",
            "fieldname": "total_paid",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Balance",
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    return columns, data