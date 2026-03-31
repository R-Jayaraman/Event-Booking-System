<div style="font-family: Arial; line-height: 1.6;">

    <h3>Booking Request Received</h3>

    <p>Dear {{ doc.customer_name or "Customer" }},</p>

    <p>Your booking request <b>{{ doc.name }}</b> has been successfully received.</p>

    <p>
        <b>Event Category:</b> {{ doc.event_category }}<br>
        <b>Venue:</b> {{ doc.venue }}<br>
        <b>Event Date:</b> {{ doc.from_date }}{% if doc.to_date %} to {{ doc.to_date }}{% endif %}
    </p>

    <p>Our team will review your request and get back to you shortly.</p>

    <br>
    <p>Thank you,<br><b>BookMyVenue Team</b></p>

</div>