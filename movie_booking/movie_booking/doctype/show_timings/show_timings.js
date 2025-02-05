// Copyright (c) 2025, Sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Show Timings", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Show Timings', {
    refresh: function(frm) {
        // Add the Reschedule button to the form
        frm.add_custom_button(__('Reschedule Show'), function() {
            frm.call('reschedule_show').then(r => {
                frappe.msgprint(__('Show has been rescheduled and all related bookings deleted.'));
            }).catch(err => {
                frappe.msgprint(__('An error occurred while rescheduling the show.'));
            });
        });
    }
});
