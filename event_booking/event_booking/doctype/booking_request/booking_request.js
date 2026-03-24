frappe.ui.form.on('Booking Request', {
    before_workflow_action: function(frm) {

        if (frm.selected_workflow_action === "Reject") {

            frappe.validated = false;

            frappe.prompt([
                {
                    label: 'Rejection Reason',
                    fieldname: 'rejection_reason',
                    fieldtype: 'Small Text',
                    reqd: 1
                }
            ],
            function(values) {

                frm.set_value('rejection_reason', values.rejection_reason);

                frm.save();
            },
            'Enter Rejection Reason',
            'Submit');

        }
    }
});
