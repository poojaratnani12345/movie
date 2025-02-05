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
