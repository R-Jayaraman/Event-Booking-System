import frappe

def get_context(context):
    cert_id = frappe.form_dict.get("certificate_id")

    doc = frappe.get_all(
    "Booking Request",
    filters={"certificate_id": cert_id},
    fields=[
        "customer_name",
        "event_category",
        "from_date",
        "qr_code",
        "certificate_id"
    ]
)

    context.data = doc[0] if doc else None