import frappe
from frappe.model.document import Document

class ShowTimings(Document):
    @frappe.whitelist()
    def reschedule_show(self):
        # Find all bookings associated with this show
        bookings = frappe.get_all('Bookings', filters={'show_time': self.name})

        # Process each booking
        for booking in bookings:
            booking_doc = frappe.get_doc('Bookings', booking['name'])

            # Check if the booking is submitted, and if so, cancel it
            if booking_doc.docstatus == 1:
                booking_doc.cancel()

            # Unlink the booking from Booking_History
            frappe.db.set_value('Booking_History', {'booking_id': booking['name']}, 'booking_id', None)

            # Explicitly delete the Booking document
            try:
                frappe.delete_doc('Bookings', booking['name'], ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Error while deleting booking {booking['name']}: {str(e)}", "Reschedule Show Error")

        # After rescheduling the show, reset available seats to total seats
        self.available_seats = self.total_seats
        self.save()

        frappe.msgprint(f"All bookings have been cancelled and deleted, and the show '{self.movie_name}' has been rescheduled.")
