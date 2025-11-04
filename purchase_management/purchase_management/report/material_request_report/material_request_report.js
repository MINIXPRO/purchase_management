// Copyright (c) 2025, Pragati Dike and contributors
// For license information, please see license.txt

frappe.query_reports["Material Request Report"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "material_request",
            "label": __("Material Request No"),
            "fieldtype": "Link",
            "options": "Material Request"
        },
        {
            "fieldname": "purchase_order",
            "label": __("Purchase Order No"),
            "fieldtype": "Link",
            "options": "Purchase Order"
        },
        {
            "fieldname": "purchase_invoice",
            "label": __("Purchase Invoice No"),
            "fieldtype": "Link",
            "options": "Purchase Invoice"
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier"
        },
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item"
        }
    ]
};
