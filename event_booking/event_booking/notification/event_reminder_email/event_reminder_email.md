<div style="font-family: Arial; line-height: 1.6;">

    <h3>Upcoming Event Reminder</h3>

    <p>Dear {{ doc.customer_name or "Customer" }},</p>

    <p>This is a reminder that your event <b>{{ doc.name }}</b> is scheduled soon.</p>

    <p>
        <b>Venue:</b> {{ doc.venue }}<br>
        <b>Date:</b> {{ doc.from_date }}<br>
        <b>Guest Count:</b> {{ doc.guest_count or 0 }}
    </p>

    <p>We look forward to making your event a success!</p>

    <br>
    <p>Thank you,<br><b>BookMyVenue Team</b></p>

</div>
