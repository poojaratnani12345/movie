# Bookings.py file:-


from datetime import datetime
from pydoc import doc
import frappe
from frappe.commands.utils import execute
from frappe.model.document import Document
from frappe import _, enqueue
from frappe.utils.data import nowdate
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf
from movie_booking.movie_booking.report.payment.payment import execute

class Bookings(Document):
    def delete_booking(self):
        """Delete the booking from the database, bypassing linked document checks."""
        try:
            # Get all linked Booking History records
            booking_history = frappe.get_all("Booking_History", filters={"booking_id": self.name})
            
            for history in booking_history:
                # Fetch the document
                history_doc = frappe.get_doc("Booking_History", history.name)

                # Correct permission check
                if history_doc.has_permission("delete"):
                    frappe.delete_doc("Booking_History", history.name)
                else:
                    return {'message': 'You do not have permission to delete the linked Booking History document.'}

            # Force delete the current Booking document
            self.delete(force=True)

            return {'message': 'Booking and linked history have been successfully deleted from the database.'}

        except Exception as e:
            frappe.log_error(f"Error deleting booking {self.name}: {str(e)}", "Delete Booking Error")
            return {'message': f"An error occurred: {str(e)}"}
        
        
    def on_cancel(self):
        # Add any logic needed when a booking is canceled
        frappe.throw("Booking has been canceled.")

        
    def before_submit(self):
        print("before submit is callinggggggggggg")
        # status=frappe.get_doc("Bookings",self.booking_status)
        
        self.booking_status = "Confirmed"

    

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
        frappe.throw(frappe._("Booking date must be less than the show time."))


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
    
    member = frappe.get_value("Member", doc.member, "email")

    subject = f"Booking Confirmation - {doc.movie}"
    message = f"""
            <p>Dear </p>
            <p>Your booking  has been successfully confirmed.</p>
            <p><b>Total Cost:</b> {doc.total_cost}</p>
    #         <p>Thank you for booking with us!</p>
    #     """
    
    print("DEBUG: doc type ->", type(doc))
    print("DEBUG: doc contents ->", doc)
    # Generate PDF
    file_doc = generate_payment_report_pdf(doc)  # Pass the doc object directly
    print("PDF generated:", file_doc)    
    print("pdf generateddddddddd:",file_doc)
    
    frappe.sendmail(
            recipients=[member],  # Send email to the user
            subject=subject,
        message=message,
        attachments=[{
            "fname": file_doc.file_name,
            "fcontent": file_doc.get_content() 
        }]
        )
    frappe.msgprint(f"Payment Report Sent to {member}!")

    print("mail senddeddddddddd")

       # Process email queue immediately
    enqueue("frappe.email.queue.flush")
# In Booking History Python code

def get_user_booking_history(user):
    # Fetch Booking History records for the logged-in user
    return frappe.get_all('Booking History', filters={'user': user}, fields=['name', 'movie', 'show_time', 'seats_booked', 'total_cost', 'booking_date'])


def generate_payment_report_pdf(doc):
    frappe.logger().info(f"Generating payment report for: {doc.member}")

    file_name = f"Payment_Report_{doc.member}.pdf"
    frappe.logger().info(f"Generating payment report for: {doc.member}")

    template_path = "movie_booking/movie_booking/print_format/format/format.html"
    html_template = frappe.get_template(template_path).render({
        "member": doc.member,
        "movie": doc.movie,
        "show_time": doc.show_time,
        "seats": doc.seats,
        "total_cost": doc.total_cost,
        "date": frappe.utils.nowdate()
    })
    pdf_content = get_pdf(html_template)


    # Save the file under the 'File' Doctype linked to the Booking
    file_doc = save_file(file_name, pdf_content, doc.doctype, doc.name, is_private=1)

    return file_doc
