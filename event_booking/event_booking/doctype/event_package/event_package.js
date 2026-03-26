const flt = frappe.utils.flt;
frappe.ui.form.on('Event Package', {
    refresh: function(frm) {
        calculate_total(frm);
    }
});

frappe.ui.form.on('Event Package Item', {

    amount: function(frm, cdt, cdn) {
        calculate_total(frm);
    },

    services_add: function(frm) {
        calculate_total(frm);
    },

    services_remove: function(frm) {
        calculate_total(frm);
    }

});

function calculate_total(frm) {
    let total = 0;

    (frm.doc.services || []).forEach(row => {
        total += flt(row.amount);
    });

    frm.set_value("total_price", total);
}