// Copyright (c) 2026, Ram and contributors
// For license information, please see license.txt

frappe.ui.form.on("Booking Payment", {
	booking(frm) {
        balance_amount = frm.doc.total_amount-frm.doc.settled_amount;
        frm.set_value("balance_amount", balance_amount);
	},
    paid_amount(frm) {
        if (frm.doc.paid_amount > frm.doc.balance_amount) {
            frappe.msgprint("Paid amount cannot be greater than balance amount.");
            frm.set_value("paid_amount", 0);
        }
    }
});
