frappe.ui.form.on("Booking Payment", {

    booking(frm) {

        update_balance(frm);
    },

    paid_amount(frm) {

        update_balance(frm);
    }
});


function update_balance(frm) {

    let total_amount = flt(frm.doc.total_amount || 0);

    let settled_amount = flt(frm.doc.settled_amount || 0);

    let paid_amount = flt(frm.doc.paid_amount || 0);

    // current balance
    let current_balance = total_amount - settled_amount;

    // validation
    if (paid_amount > current_balance) {

        frappe.msgprint("Paid amount cannot be greater than balance amount.");

        frm.set_value("paid_amount", 0);

        frm.set_value("balance_amount", current_balance);

        return;
    }

    // preview balance after payment
    let new_balance = total_amount - (settled_amount + paid_amount);

    frm.set_value("balance_amount", new_balance);
}