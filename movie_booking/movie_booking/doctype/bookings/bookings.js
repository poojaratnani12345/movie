// Copyright (c) 2025, Sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Bookings", {
// 	refresh(frm) {

// 	},
// });
// In your client-side script (e.g., bookings.js)

// In your client-side script (e.g., bookings.js)
// In your client-side script (e.g., bookings.js)

frappe.ui.form.on('Bookings', {
    refresh: function(frm) {
        frm.add_custom_button(__('delete_booking'), function() {
            // Ask for user confirmation before deletion
            frappe.confirm(
                __('Are you sure you want to cancel and delete this booking?'),
                function() {
                    // Call the delete method defined in Bookings.py
                    frm.call('delete_booking')
                        .then(response => {
                            frappe.msgprint(response.message);  // Show success message
                            frm.reload_doc();  // Reload the form to reflect the changes
                        })
                        .catch(error => {
                            frappe.msgprint(__('An error occurred while deleting the booking.'));
                        });
                }
            );
        });
    }
});
frappe.ui.form.on('Bookings', {
    payment_method: function (frm) {
        if (frm.doc.payment_method === "Credit Card") {
            // Show and make credit card fields required
            frm.set_df_property("card_number", "hidden", 0);
            frm.set_df_property("expiry_date", "hidden", 0);
            frm.set_df_property("cvv", "hidden", 0);

            frm.set_df_property("card_number", "reqd", 1);
            frm.set_df_property("exp_date", "reqd", 1);
            frm.set_df_property("cvv", "reqd", 1);
        } else {
            // Hide and make credit card fields non-required for other payment methods
            frm.set_df_property("card_number", "hidden", 1);
            frm.set_df_property("expiry_date", "hidden", 1);
            frm.set_df_property("cvv", "hidden", 1);

            frm.set_df_property("card_number", "reqd", 0);
            frm.set_df_property("expiry_date", "reqd", 0);
            frm.set_df_property("cvv", "reqd", 0);
        }
    }
});
