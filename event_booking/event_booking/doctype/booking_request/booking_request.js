let global_tax = 0;

frappe.ui.form.on('Booking Request', {

    onload: function(frm) {

        frm.set_query("event_category", function () {
            return {
                filters: {
                    is_group: 0
                }
            };
        });

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Event Booking Settings",
                filters: {},
                fieldname: "default_tax"
            },
            callback: function(r) {
                global_tax = r.message.default_tax || 0;
                calculate_cost(frm);
            }
        });
    },

    refresh: function(frm) {
        calculate_cost(frm);
    },

    before_workflow_action: function(frm) {

        if (frm.selected_workflow_action === "Reject") {

            frappe.validated = false;

            frappe.prompt(
                [
                    {
                        fieldname: 'rejection_reason',
                        label: 'Reason for Rejection',
                        fieldtype: 'Small Text',
                        reqd: 1
                    }
                ],
                function(values) {

                    frm.set_value('rejection_reason', values.rejection_reason);

                    frm.save().then(() => {

                        frappe.validated = true;

                        frm.page.btn_primary.trigger("click");
                    });

                },
                  ('Enter Rejection Reason'),
                  ('Submit')
            );
        }
    },

    event_category: function(frm) {

        frm.set_query("event_package", function () {
            return {
                filters: {
                    event_category: frm.doc.event_category
                }
            };
        });

        frm.set_value("event_package", null);
        frm.clear_table("services");
        frm.refresh_field("services");
    },

    event_package: function(frm) {
        if (frm.doc.event_package) {
            fetch_package_services(frm);
            fetch_package_cost(frm);
        }
    },

    venue_cost: calculate_cost,
    package_cost: calculate_cost,
    profit_margin: calculate_cost,
    discount: calculate_cost
});


function fetch_package_services(frm) {
    frappe.call({
        method: "event_booking.event_booking.doctype.booking_request.booking_request.get_package_services",
        args: {
            package: frm.doc.event_package
        },
        callback: function(r) {
            if (r.message) {

                frm.clear_table("services");

                r.message.forEach(item => {
                    let row = frm.add_child("services");
                    row.service_provider = item.service_provider;
                    row.service_type = item.service_type;
                    row.cost = item.cost;
                });

                frm.refresh_field("services");
            }
        }
    });
}


function fetch_package_cost(frm) {
    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "Event Package",
            filters: { name: frm.doc.event_package },
            fieldname: "total_price"
        },
        callback: function(r) {
            if (r.message) {
                frm.set_value("package_cost", r.message.total_price);
                calculate_cost(frm);
            }
        }
    });
}


function calculate_cost(frm) {

    let venue_cost = flt(frm.doc.venue_cost);
    let package_cost = flt(frm.doc.package_cost);

    let subtotal = venue_cost + package_cost;

    let profit_margin = flt(frm.doc.profit_margin);
    let profit_amount = subtotal * (profit_margin / 100);

    let tax_amount = subtotal * (global_tax / 100);

    let total_amount = subtotal + profit_amount + tax_amount;

    let discount = flt(frm.doc.discount);
    let final_amount = total_amount - discount;

    frm.set_value("profit_amount", profit_amount);
    frm.set_value("tax_amount", tax_amount);
    frm.set_value("total_amount", total_amount);
    frm.set_value("final_amount", final_amount);

    frm.refresh_field("profit_amount");
    frm.refresh_field("tax_amount");
    frm.refresh_field("total_amount");
    frm.refresh_field("final_amount");
}