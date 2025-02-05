from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe import _

class Bookings(Document): 
    @frappe.whitelist()
    def delete_booking(self):
        """Delete the booking from the database, bypassing linked document checks."""
        try:
            # Check if the current user has permission to delete the linked Booking History
            booking_history = frappe.get_all("Booking_History", filters={"booking_id": self.name})
            for history in booking_history:
                # Check if the user has permissions to delete this Booking History
                history_doc = frappe.get_doc("Booking_History", history.name)
                if history_doc.get_permissions("delete"):
                    frappe.delete_doc("Booking_History", history.name)
                else:
                    return {'message': 'You do not have permission to delete the linked Booking History document.'}
            
            # Force delete the current Booking document
            self.delete(force=True)
            
            return {'message': 'Booking and linked history have been successfully deleted from the database.'}

        except Exception as e:
            frappe.log_error(f"Error deleting booking {self.name}: {str(e)}", "Delete Booking Error")
            return {'message': f"An error occurred: {str(e)}"}

def validate(doc, method):
    # Define ticket price (this can be dynamic if needed)
    ticket_price = 100  # Replace this with dynamic logic if necessary

    # Calculate the total cost based on seats booked
    doc.total_cost = doc.seats * ticket_price

    # Get the Show Timing document only once
    show_timing = frappe.get_doc('Show Timings', doc.show_time)

    # Validate seat availability
    if doc.seats > show_timing.available_seats:
        frappe.throw(f"Not enough seats available! Only {show_timing.available_seats} seats left.")

    # Convert booking_date to datetime if it's a string
    if isinstance(doc.booking_date, str):
        doc.booking_date = datetime.strptime(doc.booking_date, '%Y-%m-%d %H:%M:%S')
    
    # Compare Booking Date with Show Time
    if doc.booking_date <= show_timing.show_time:
        frappe.throw(frappe._("Booking date must be greater than the show time."))


def on_submit(doc, method):
    # Fetch the linked show timing
    show_timing = frappe.get_doc('Show Timings', doc.show_time)

    # Update available seats only on submission
    if show_timing.available_seats >= doc.seats:
        show_timing.available_seats -= doc.seats
        show_timing.save()
    else:
        frappe.throw("Not enough seats available for this booking.")


    # Store information in Booking History
    booking_history = frappe.get_doc({
        "doctype": "Booking_History",
        "booking_id": doc.name,
        "user": doc.member,  # This assumes the owner of the booking is the user who booked the tickets
        "movie": doc.movie,
        "show_timing": doc.show_time,
        "seats_booked": doc.seats,
        "total_cost": doc.total_cost,
        "booking_date": doc.booking_date  # Current date and time
    })

    # Insert the new booking history entry
    booking_history.insert(ignore_permissions=True)

# In Booking History Python code

def get_user_booking_history(user):
    # Fetch Booking History records for the logged-in user
    return frappe.get_all('Booking History', filters={'user': user}, fields=['name', 'movie', 'show_time', 'seats_booked', 'total_cost', 'booking_date'])
