frappe.ui.form.on('Booking Request', {

    onload: function(frm) {

        frm.set_query("event_category", function () {
            return {
                filters: { is_group: 0 }
            };
        });

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Event Booking Settings",
                filters: {},
                fieldname: "default_tax"
            },
            callback: function(res) {
                frm.tax_rate = (res.message && res.message.default_tax) || 0;
            }
        });
    },

    from_date: function(frm) { update_preview(frm); },
    to_date: function(frm) { update_preview(frm); },
    venue: function(frm) { update_preview(frm); },
    profit_margin: function(frm) { update_preview(frm); },
    discount: function(frm) { update_preview(frm); },

    event_package: function(frm) {
        load_package_services(frm);
        update_preview(frm);
    },

    before_workflow_action: function(frm) {

        if (frm.selected_workflow_action === "Reject") {

            frappe.validated = false;

            frappe.prompt(
                [
                    {
                        fieldname: "rejection_reason",
                        label: "Reason for Rejection",
                        fieldtype: "Small Text",
                        reqd: 1
                    }
                ],
                function(values) {

                    frm.set_value("rejection_reason", values.rejection_reason);

                    frm.save().then(() => {
                        frappe.validated = true;
                        frm.page.btn_primary.trigger("click");
                    });

                },
                "Enter Rejection Reason",
                "Submit"
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
    }

});

function load_package_services(frm) {

    if (!frm.doc.event_package) return;

    frappe.call({
        method: "event_booking.event_booking.doctype.booking_request.booking_request.get_package_services",
        args: {
            package: frm.doc.event_package
        },
        callback: function(res) {

            if (!res.message) return;

            frm.clear_table("services");

            res.message.forEach(service => {
                let row = frm.add_child("services");
                row.service_provider = service.service_provider;
                row.service_type = service.service_type;
                row.cost = service.cost;
            });

            frm.refresh_field("services");
        }
    });
}

function update_preview(frm) {

    if (!(frm.doc.venue && frm.doc.from_date && frm.doc.to_date)) return;

    let from = frappe.datetime.str_to_obj(frm.doc.from_date);
    let to = frappe.datetime.str_to_obj(frm.doc.to_date);

    let total_days = frappe.datetime.get_day_diff(to, from) + 1;

    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "Venue",
            filters: { name: frm.doc.venue },
            fieldname: "daily_rate"
        },
        callback: function(res) {

            let rate = (res.message && res.message.daily_rate) || 0;
            let venue_cost = rate * total_days;

            frm.set_value("venue_cost", venue_cost);

            if (frm.doc.event_package) {

                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Event Package",
                        filters: { name: frm.doc.event_package },
                        fieldname: "total_price"
                    },
                    callback: function(pkg) {

                        let pkg_cost = (pkg.message && pkg.message.total_price) || 0;

                        frm.set_value("package_cost", pkg_cost);

                        update_totals(frm);
                    }
                });

            } else {
                update_totals(frm);
            }
        }
    });
}

function update_totals(frm) {

    let venue = flt(frm.doc.venue_cost);
    let pkg = flt(frm.doc.package_cost);

    let subtotal = venue + pkg;

    let margin = flt(frm.doc.profit_margin);
    let profit = subtotal * (margin / 100);

    let tax = subtotal * ((frm.tax_rate || 0) / 100);

    let total = subtotal + profit + tax;

    let discount = flt(frm.doc.discount);
    let final = total - discount;

    frm.set_value("profit_amount", profit);
    frm.set_value("tax_amount", tax);
    frm.set_value("total_amount", total);
    frm.set_value("final_amount", final);
}