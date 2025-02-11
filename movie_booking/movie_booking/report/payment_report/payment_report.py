
from frappe import _
import frappe


def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data(filters)
    
	total_revenue=sum(row['total_cost'] for row in data if row['booking_status']=="Pending")
    
	summary_row={
        "member": "Total",
        "movie": "",
        "payment_method": "",
        "total_cost": total_revenue,
        "booking_status": "Confirmed",
        "booking_date": "",
	}
	data.append(summary_row)
	return columns, data


def get_columns():
    return [
		{"label":"Member","fieldname":"member","fieldtype":"Data","width":200},
        {"label": "Movie Name", "fieldname": "movie", "fieldtype": "Data", "width": 200},
        {"label": "Payment Method", "fieldname": "payment_method", "fieldtype": "Data", "width": 150},
        {"label": "Total Amount", "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Payment Status", "fieldname": "booking_status", "fieldtype": "Data", "width": 120},
		{"label": "Transaction Date", "fieldname": "booking_date", "fieldtype": "Date", "width": 120},

    ]


def get_data(filters):
    conditions = "1=1"
    if filters.get("member"):
        conditions += f" AND b.member = '{filters.get('member')}'"
    if filters.get("movie"):
        conditions += f" AND b.movie = '{filters.get('movie')}'"
    if filters.get("payment_method"):
        conditions += f" AND b.payment_method = '{filters.get('payment_method')}'"
    if filters.get("payment_status"):
        conditions += f" AND b.booking_status = '{filters.get('payment_status')}'"
    if filters.get("booking_date"):
        conditions += f" AND b.booking_date = '{filters.get('booking_date')}'"

    query = f"""
        SELECT 
            b.member, b.movie, b.payment_method, 
            b.total_cost, b.booking_status, b.booking_date
        FROM `tabBookings` b
        WHERE {conditions}
        ORDER BY b.booking_date DESC
    """
    
    return frappe.db.sql(query, as_dict=True)

def get_summary(data):
    total_success = sum(row["total_cost"] for row in data if row["booking_status"] == "Success")
    total_failed = sum(row["total_cost"] for row in data if row["booking_status"] == "Failed")
    
    return [
        {"label": "Total Revenue (Success)", "value": total_success, "indicator": "Green"},
        {"label": "Total Failed Transactions", "value": total_failed, "indicator": "Red"}
    ]


def get_filters():
    return [
        {
            "fieldname": "member",
            "label": "Member",
            "fieldtype": "Data",
            "options": "Member"
        },
        {
            "fieldname": "movie",
            "label": "Movie Name",
            "fieldtype": "Data",
            "options": "Movies"
        },
        {
            "fieldname": "payment_method",
            "label": "Payment Method",
            "fieldtype": "Select",
            "options": "\nCredit Card\nUPI\nWallet\nCash"
        },
        {
            "fieldname": "payment_status",
            "label": "Payment Status",
            "fieldtype": "Select",
            "options": "\nSuccess\nFailed"
        },
        
    ]
