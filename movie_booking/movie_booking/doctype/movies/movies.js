// Copyright (c) 2025, Sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Movies", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Movies', {
    refresh: function(frm) {
        frm.fields_dict['show_tables'].grid.get_field('show_time').get_query = function() {
            return {
                filters: {
                    movie_name: frm.doc.movie_name  // Filter show timings by the current movie
                }
            };
        };
    }
});
frappe.ui.form.on('Movies', {
    on_submit: function(frm) {
        console.log("Submitting Movie form...");

        // Check if the child table 'booking_details' exists and has rows
        if (!frm.doc.show_tables || frm.doc.booking_details.length === 0) {
            console.log("No child table rows found.");
            return;
        }

        // Loop through the child table rows
        frm.doc.booking_details.forEach(function(row) {
            console.log("Processing row: ", row);
            if (row.movie) {
                frappe.db.get_value('Movies', row.movie, 'title', function(value) {
                    console.log("Fetched Movie Title: ", value.title);
                    frappe.model.set_value(row.doctype, row.name, 'Movie', value.title);
                });
            }
        });

        // Save the changes made in the child table
        frm.save();
    }
});
