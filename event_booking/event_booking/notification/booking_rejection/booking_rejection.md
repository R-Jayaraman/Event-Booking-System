<div style="font-family: Arial; line-height: 1.6;">
    <h3 style="color:red;">Booking Rejected</h3>

    <p>Dear {{ doc.customer_name }},</p>

    <p>We regret to inform you that your booking <b>{{ doc.name }}</b> has been rejected.</p>

    <p>
        <b>Reason:</b><br>
        {{ doc.rejection_reason }}
    </p>

    <p>You may update your request and resubmit it.</p>

    <br>
    <p>Thank you,<br>BookMyVenue Team</p>
</div>