<div style="font-family: Arial; line-height: 1.6;">
    <h3>Booking Confirmed</h3>

    <p>Dear {{ doc.customer_name }},</p>

    <p>Your booking <b>{{ doc.name }}</b> has been <b style="color:green;">approved</b>.</p>

    <p>
        <b>Venue:</b> {{ doc.venue }}<br>
        <b>Event Date:</b> {{ doc.from_date }} to {{ doc.to_date }}<br>
        <b>Total Amount:</b> {{ doc.final_amount }}
    </p>

    <p>Please proceed with the payment to confirm your booking.</p>

    <br>
    <p>We look forward to hosting your event!</p>

    <br>
    <p>Thank you,<br>BookMyVenue Team</p>
</div>
