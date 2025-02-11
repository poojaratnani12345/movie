// Copyright (c) 2025, Sarvadhi and contributors
// For license information, please see license.txt

frappe.query_reports["Payment"] = {
	filters: [
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
            "options": "\nConfirmed\nPending"
        },
		
	],
};
