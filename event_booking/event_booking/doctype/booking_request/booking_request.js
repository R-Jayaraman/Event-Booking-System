frappe.ui.form.on('Booking Request', {

    onload: function(frm) {

        frm.set_query("event_category", function () {
            return {
                filters: {
                    is_group: 0
                }
            };
        });

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
            calculate_cost(frm);
        }
    },

    venue: calculate_cost,
    from_date: calculate_cost,
    to_date: calculate_cost,
    discount: calculate_cost,
    package_cost: calculate_cost
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
            }
        }
    });
}

function calculate_cost(frm) {

    if (!frm.doc.venue || !frm.doc.from_date || !frm.doc.to_date) return;

    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "Venue",
            filters: { name: frm.doc.venue },
            fieldname: "daily_rate"
        },
        callback: function(r) {

            let rate = r.message.daily_rate || 0;

            let from_date = new Date(frm.doc.from_date);
            let to_date = new Date(frm.doc.to_date);

            let days = ((to_date - from_date) / (1000 * 60 * 60 * 24)) + 1;

            let venue_cost = rate * days;
            let package_cost = frm.doc.package_cost || 0;

            let subtotal = venue_cost + package_cost;

            let tax_percent = 18;
            let tax_amount = subtotal * (tax_percent / 100);

            let total_amount = subtotal + tax_amount;

            let discount = frm.doc.discount || 0;
            let final_amount = total_amount - discount;

            frm.set_value("venue_cost", venue_cost);
            frm.set_value("tax_amount", tax_amount);
            frm.set_value("total_amount", total_amount);
            frm.set_value("final_amount", final_amount);
        }
    });
}