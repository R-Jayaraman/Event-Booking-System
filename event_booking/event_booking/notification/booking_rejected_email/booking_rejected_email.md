<div style="font-family: Arial; line-height: 1.6;">
    <h3 style="color:red;">Booking Rejected</h3>

    <p>Dear {{ doc.customer_name }},</p>

    <p>We regret to inform you that your booking <b>{{ doc.name }}</b> has been rejected.</p>

    {% set d = frappe.get_doc(doc.doctype, doc.name) %}

    <p>
        <b>Reason:</b><br>
        {{ d.rejection_reason or "Not provided" }}
    </p>

    <p>You may update your request and resubmit it.</p>

    <br>
    <p>Thank you,<br>BookMyVenue Team</p>
</div>