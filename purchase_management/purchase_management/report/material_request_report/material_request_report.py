# # Copyright (c) 2025, Pragati Dike and contributors
# # For license information, please see license.txt

# import frappe
# from frappe import _
# from frappe.utils import flt, getdate, get_datetime, time_diff_in_seconds

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     """Define report columns"""
#     return [
#         {
#             "fieldname": "sno",
#             "label": _("S.No"),
#             "fieldtype": "Int",
#             "width": 60
#         },
#         {
#             "fieldname": "mr_no",
#             "label": _("MR No."),
#             "fieldtype": "Link",
#             "options": "Material Request",
#             "width": 150
#         },
#         {
#             "fieldname": "mr_date",
#             "label": _("MR Date"),
#             "fieldtype": "Datetime",
#             "width": 150
#         },
#         {
#             "fieldname": "schedule_date",
#             "label": _("Requested By / Dept."),
#             "fieldtype": "Data",
#             "width": 150
#         },
#         {
#             "fieldname": "item_code",
#             "label": _("Item Code"),
#             "fieldtype": "Link",
#             "options": "Item",
#             "width": 120
#         },
#         {
#             "fieldname": "item_name",
#             "label": _("Item Name"),
#             "fieldtype": "Data",
#             "width": 180
#         },
#         {
#             "fieldname": "required_qty",
#             "label": _("Required Qty"),
#             "fieldtype": "Float",
#             "width": 100
#         },
#         {
#             "fieldname": "po_no",
#             "label": _("PO No."),
#             "fieldtype": "Link",
#             "options": "Purchase Order",
#             "width": 150
#         },
#         {
#             "fieldname": "po_date",
#             "label": _("PO Date"),
#             "fieldtype": "Datetime",
#             "width": 150
#         },
#         {
#             "fieldname": "vendor_name",
#             "label": _("Vendor Name"),
#             "fieldtype": "Link",
#             "options": "Supplier",
#             "width": 150
#         },
#         {
#             "fieldname": "ordered_qty",
#             "label": _("Ordered Qty"),
#             "fieldtype": "Float",
#             "width": 100
#         },
#         {
#             "fieldname": "received_qty",
#             "label": _("Received Qty (GRN)"),
#             "fieldtype": "Float",
#             "width": 120
#         },
#         {
#             "fieldname": "grn_date",
#             "label": _("GRN Date"),
#             "fieldtype": "Datetime",
#             "width": 150
#         },
#         {
#             "fieldname": "remaining_qty",
#             "label": _("Remaining Qty"),
#             "fieldtype": "Float",
#             "width": 100
#         },
#         {
#             "fieldname": "invoice_no",
#             "label": _("Invoice No."),
#             "fieldtype": "Link",
#             "options": "Purchase Invoice",
#             "width": 150
#         },
#         {
#             "fieldname": "invoice_date",
#             "label": _("Invoice Date"),
#             "fieldtype": "Datetime",
#             "width": 150
#         },
#         {
#             "fieldname": "mr_to_po_time",
#             "label": _("MR → PO"),
#             "fieldtype": "Data",
#             "width": 120
#         },
#         {
#             "fieldname": "po_to_grn_time",
#             "label": _("PO → GRN"),
#             "fieldtype": "Data",
#             "width": 120
#         },
#         {
#             "fieldname": "grn_to_pi_time",
#             "label": _("GRN → PI"),
#             "fieldtype": "Data",
#             "width": 120
#         },
#         {
#             "fieldname": "total_lead_time",
#             "label": _("Total Lead Time"),
#             "fieldtype": "Data",
#             "width": 150
#         },
#         {
#             "fieldname": "rate",
#             "label": _("Rate / Unit"),
#             "fieldtype": "Currency",
#             "width": 100
#         },
#         {
#             "fieldname": "po_value",
#             "label": _("PO Value (₹)"),
#             "fieldtype": "Currency",
#             "width": 120
#         },
#         {
#             "fieldname": "invoice_amount",
#             "label": _("Invoice Amount (₹)"),
#             "fieldtype": "Currency",
#             "width": 120
#         },
#         {
#             "fieldname": "mr_status",
#             "label": _("MR Status"),
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "fieldname": "po_status",
#             "label": _("PO Status"),
#             "fieldtype": "Data",
#             "width": 100
#         },
#         {
#             "fieldname": "invoice_status",
#             "label": _("Invoice Status"),
#             "fieldtype": "Data",
#             "width": 120
#         }
#     ]

# def format_time_difference(seconds):
#     """
#     Format time difference in appropriate units
#     Returns string in format: X days, X hrs, or X mins
#     """
#     if not seconds or seconds < 0:
#         return ""
    
#     days = seconds // 86400
#     hours = (seconds % 86400) // 3600
#     minutes = (seconds % 3600) // 60
    
#     if days >= 1:
#         if hours > 0:
#             return f"{int(days)}d {int(hours)}h"
#         return f"{int(days)} days"
#     elif hours >= 1:
#         if minutes > 0:
#             return f"{int(hours)}h {int(minutes)}m"
#         return f"{int(hours)} hrs"
#     elif minutes >= 1:
#         return f"{int(minutes)} mins"
#     else:
#         return "< 1 min"

# def get_workflow_transition_time(doctype, docname, from_state, to_state):
#     """
#     Get the time when a document transitioned from one workflow state to another
#     """
#     try:
#         # Get workflow logs for state transitions
#         logs = frappe.db.sql("""
#             SELECT creation, data
#             FROM `tabVersion`
#             WHERE ref_doctype = %s
#                 AND docname = %s
#                 AND data LIKE %s
#             ORDER BY creation ASC
#         """, (doctype, docname, f'%{to_state}%'), as_dict=1)
        
#         if logs:
#             for log in logs:
#                 # Parse the data to check if it's the right transition
#                 if to_state in str(log.data):
#                     return log.creation
        
#         # Fallback: Get document creation/modified time based on workflow_state
#         doc_data = frappe.db.get_value(
#             doctype, 
#             docname, 
#             ['workflow_state', 'creation', 'modified'], 
#             as_dict=1
#         )
        
#         if doc_data and doc_data.workflow_state == to_state:
#             return doc_data.modified
            
#     except Exception as e:
#         frappe.log_error(f"Error getting workflow transition time: {str(e)}")
    
#     return None

# def get_mr_approval_time(mr_no):
#     """
#     Get the time when MR was approved (workflow state changed to approved)
#     For Material Request, the approved state is "Approved From Function Head"
#     """
#     # First try to get from workflow history
#     approval_time = get_workflow_transition_time(
#         "Material Request", 
#         mr_no, 
#         "Pending Approval From Function Head",
#         "Approved From Function Head"
#     )
    
#     if approval_time:
#         return approval_time
    
#     # Fallback: Get modified time when docstatus = 1
#     mr_data = frappe.db.sql("""
#         SELECT modified
#         FROM `tabMaterial Request`
#         WHERE name = %s AND docstatus = 1
#     """, mr_no, as_dict=1)
    
#     return mr_data[0].modified if mr_data else None

# def get_po_approval_time(po_no):
#     """
#     Get the time when PO was approved
#     For Purchase Order, the approved state is "Approved By Purchase Head"
#     """
#     approval_time = get_workflow_transition_time(
#         "Purchase Order",
#         po_no,
#         "Pending Approval Of Purchase Head",
#         "Approved By Purchase Head"
#     )
    
#     if approval_time:
#         return approval_time
    
#     # Fallback: Get modified time when docstatus = 1
#     po_data = frappe.db.sql("""
#         SELECT modified
#         FROM `tabPurchase Order`
#         WHERE name = %s AND docstatus = 1
#     """, po_no, as_dict=1)
    
#     return po_data[0].modified if po_data else None

# def get_data(filters):
#     """Fetch and process data"""
#     conditions = get_conditions(filters)
    
#     # Main query to get Material Request items with workflow timestamps
#     query = """
#         SELECT
#             mri.parent as mr_no,
#             mr.creation AS mr_creation,
#             mr.modified AS mr_modified,
#             mr.schedule_date AS schedule_date,
#             mri.item_code,
#             mri.item_name,
#             mri.qty as required_qty,
#             mr.status as mr_status,
#             mr.workflow_state as mr_workflow_state,
#             mri.name as mr_item_name
#         FROM
#             `tabMaterial Request Item` mri
#         INNER JOIN
#             `tabMaterial Request` mr ON mri.parent = mr.name
#         WHERE
#             mr.docstatus = 1
#             {conditions}
#         ORDER BY
#             mr.creation DESC, mr.name
#     """.format(conditions=conditions)
    
#     mr_data = frappe.db.sql(query, filters, as_dict=1)
    
#     data = []
#     sno = 1
    
#     for mr_item in mr_data:
#         # Get MR approval time
#         mr_approved_time = get_mr_approval_time(mr_item.mr_no)
#         mr_time = mr_approved_time or mr_item.mr_modified
        
#         # Get Purchase Order details with workflow timestamps
#         po_details = get_purchase_order_details(mr_item.mr_no, mr_item.item_code)
        
#         if po_details:
#             for po in po_details:
#                 # Get PO approval time
#                 po_approved_time = get_po_approval_time(po.po_no)
#                 po_time = po_approved_time or po.po_modified
                
#                 # Get Purchase Receipt (GRN) details
#                 grn_details = get_grn_details(po.po_no, mr_item.item_code)
                
#                 # Get Purchase Invoice details
#                 pi_details = get_purchase_invoice_details(po.po_no, mr_item.item_code)
                
#                 # Calculate time differences in seconds
#                 mr_to_po_seconds = None
#                 po_to_grn_seconds = None
#                 grn_to_pi_seconds = None
#                 total_seconds = None
                
#                 if mr_time and po_time:
#                     mr_to_po_seconds = time_diff_in_seconds(po_time, mr_time)
                
#                 if po_time and grn_details.get('grn_datetime'):
#                     po_to_grn_seconds = time_diff_in_seconds(grn_details.get('grn_datetime'), po_time)
                
#                 if grn_details.get('grn_datetime') and pi_details.get('invoice_datetime'):
#                     grn_to_pi_seconds = time_diff_in_seconds(pi_details.get('invoice_datetime'), grn_details.get('grn_datetime'))
                
#                 if mr_time and pi_details.get('invoice_datetime'):
#                     total_seconds = time_diff_in_seconds(pi_details.get('invoice_datetime'), mr_time)
                
#                 remaining_qty = flt(po.ordered_qty) - flt(grn_details.get('received_qty', 0))
                
#                 row = {
#                     "sno": sno,
#                     "mr_no": mr_item.mr_no,
#                     "mr_date": mr_time,
#                     "schedule_date": mr_item.schedule_date,
#                     "item_code": mr_item.item_code,
#                     "item_name": mr_item.item_name,
#                     "required_qty": mr_item.required_qty,
#                     "po_no": po.po_no,
#                     "po_date": po_time,
#                     "vendor_name": po.supplier,
#                     "ordered_qty": po.ordered_qty,
#                     "received_qty": grn_details.get('received_qty', 0),
#                     "grn_date": grn_details.get('grn_datetime'),
#                     "remaining_qty": remaining_qty,
#                     "invoice_no": pi_details.get('invoice_no'),
#                     "invoice_date": pi_details.get('invoice_datetime'),
#                     "mr_to_po_time": format_time_difference(mr_to_po_seconds),
#                     "po_to_grn_time": format_time_difference(po_to_grn_seconds),
#                     "grn_to_pi_time": format_time_difference(grn_to_pi_seconds),
#                     "total_lead_time": format_time_difference(total_seconds),
#                     "rate": po.rate,
#                     "po_value": po.amount,
#                     "invoice_amount": pi_details.get('invoice_amount', 0),
#                     "mr_status": mr_item.mr_status,
#                     "po_status": po.status,
#                     "invoice_status": pi_details.get('invoice_status', 'Not Created')
#                 }
                
#                 data.append(row)
#                 sno += 1
#         else:
#             # No PO created yet
#             row = {
#                 "sno": sno,
#                 "mr_no": mr_item.mr_no,
#                 "mr_date": mr_time,
#                 "schedule_date": mr_item.schedule_date,
#                 "item_code": mr_item.item_code,
#                 "item_name": mr_item.item_name,
#                 "required_qty": mr_item.required_qty,
#                 "mr_status": mr_item.mr_status,
#                 "po_status": "Not Created"
#             }
#             data.append(row)
#             sno += 1
    
#     return data

# def get_conditions(filters):
#     """Build filter conditions"""
#     conditions = ""
    
#     if filters.get("from_date"):
#         conditions += " AND mr.creation >= %(from_date)s"
    
#     if filters.get("to_date"):
#         conditions += " AND mr.creation <= %(to_date)s"
    
#     if filters.get("material_request"):
#         conditions += " AND mr.name = %(material_request)s"
    
#     if filters.get("item_code"):
#         conditions += " AND mri.item_code = %(item_code)s"
    
#     if filters.get("supplier"):
#         conditions += " AND EXISTS (SELECT 1 FROM `tabPurchase Order` po INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent WHERE poi.material_request = mr.name AND po.supplier = %(supplier)s)"
    
#     return conditions

# def get_purchase_order_details(mr_no, item_code):
#     """Get Purchase Order details with timestamps"""
#     po_data = frappe.db.sql("""
#         SELECT
#             po.name as po_no,
#             po.creation as po_creation,
#             po.modified as po_modified,
#             po.supplier,
#             po.status,
#             po.workflow_state,
#             poi.qty as ordered_qty,
#             poi.rate,
#             poi.amount
#         FROM
#             `tabPurchase Order` po
#         INNER JOIN
#             `tabPurchase Order Item` poi ON po.name = poi.parent
#         WHERE
#             po.docstatus = 1
#             AND poi.material_request = %s
#             AND poi.item_code = %s
#         ORDER BY
#             po.creation DESC
#     """, (mr_no, item_code), as_dict=1)
    
#     return po_data

# def get_grn_details(po_no, item_code):
#     """Get Purchase Receipt (GRN) details with datetime"""
#     grn_data = frappe.db.sql("""
#         SELECT
#             SUM(pri.qty) as received_qty,
#             MAX(pr.posting_date) as grn_date,
#             MAX(pr.modified) as grn_datetime
#         FROM
#             `tabPurchase Receipt` pr
#         INNER JOIN
#             `tabPurchase Receipt Item` pri ON pr.name = pri.parent
#         WHERE
#             pr.docstatus = 1
#             AND pri.purchase_order = %s
#             AND pri.item_code = %s
#     """, (po_no, item_code), as_dict=1)
    
#     return grn_data[0] if grn_data else {}

# def get_purchase_invoice_details(po_no, item_code):
#     """Get Purchase Invoice details with datetime"""
#     pi_data = frappe.db.sql("""
#         SELECT
#             pi.name as invoice_no,
#             pi.posting_date as invoice_date,
#             pi.modified as invoice_datetime,
#             SUM(pii.amount) as invoice_amount,
#             pi.status as invoice_status
#         FROM
#             `tabPurchase Invoice` pi
#         INNER JOIN
#             `tabPurchase Invoice Item` pii ON pi.name = pii.parent
#         WHERE
#             pi.docstatus = 1
#             AND pii.purchase_order = %s
#             AND pii.item_code = %s
#         GROUP BY
#             pi.name
#         ORDER BY
#             pi.posting_date DESC
#         LIMIT 1
#     """, (po_no, item_code), as_dict=1)
    
#     return pi_data[0] if pi_data else {}


# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, time_diff_in_seconds
import json

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "sno",
            "label": _("S.No"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "mr_no",
            "label": _("MR No."),
            "fieldtype": "Link",
            "options": "Material Request",
            "width": 150
        },
        {
            "fieldname": "mr_date",
            "label": _("MR Date"),
            "fieldtype": "Datetime",
            "width": 150
        },
        {
            "fieldname": "schedule_date",
            "label": _("Requested By / Dept."),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 120
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "required_qty",
            "label": _("Required Qty"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "pr_no",
            "label": _("PR No."),
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 150
        },
        {
            "fieldname": "pr_date",
            "label": _("PR Date"),
            "fieldtype": "Datetime",
            "width": 150
        },
        {
            "fieldname": "po_no",
            "label": _("PO No."),
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 150
        },
        {
            "fieldname": "po_date",
            "label": _("PO Date"),
            "fieldtype": "Datetime",
            "width": 150
        },
        {
            "fieldname": "vendor_name",
            "label": _("Vendor Name"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "fieldname": "ordered_qty",
            "label": _("Ordered Qty"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "received_qty",
            "label": _("Received Qty (GRN)"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "remaining_qty",
            "label": _("Remaining Qty"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "invoice_no",
            "label": _("Invoice No."),
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 150
        },
        {
            "fieldname": "invoice_date",
            "label": _("Invoice Date"),
            "fieldtype": "Datetime",
            "width": 150
        },
        {
            "fieldname": "mr_to_pr_time",
            "label": _("MR → PR"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "pr_to_po_time",
            "label": _("PR → PO"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "po_to_grn_time",
            "label": _("PO → GRN"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "grn_to_pi_time",
            "label": _("GRN → PI"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "total_lead_time",
            "label": _("Total Lead Time"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "rate",
            "label": _("Rate / Unit"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "po_value",
            "label": _("PO Value (₹)"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "invoice_amount",
            "label": _("Invoice Amount (₹)"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "mr_status",
            "label": _("MR Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "po_status",
            "label": _("PO Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "invoice_status",
            "label": _("Invoice Status"),
            "fieldtype": "Data",
            "width": 120
        }
    ]

def format_time_difference(seconds):
    """
    Format time difference in appropriate units
    Returns string in format: X days, X hrs, or X mins
    """
    if not seconds or seconds < 0:
        return ""
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    if days >= 1:
        if hours > 0:
            return f"{int(days)}d {int(hours)}h"
        return f"{int(days)} days"
    elif hours >= 1:
        if minutes > 0:
            return f"{int(hours)}h {int(minutes)}m"
        return f"{int(hours)} hrs"
    elif minutes >= 1:
        return f"{int(minutes)} mins"
    else:
        return "< 1 min"

def get_workflow_state_timestamp(doctype, docname, target_state):
    """
    Get the timestamp when a document reached a specific workflow state
    by checking the Version/Comment logs
    """
    try:
        # Method 1: Check Version table for workflow state changes
        version_data = frappe.db.sql("""
            SELECT creation, data
            FROM `tabVersion`
            WHERE ref_doctype = %s
                AND docname = %s
            ORDER BY creation ASC
        """, (doctype, docname), as_dict=1)
        
        for version in version_data:
            if version.data:
                try:
                    # Parse the version data
                    data = json.loads(version.data)
                    if data.get('changed'):
                        for change in data['changed']:
                            # Check if workflow_state changed to target state
                            if (change[0] == 'workflow_state' and 
                                len(change) > 2 and 
                                change[2] == target_state):
                                return get_datetime(version.creation)
                except:
                    # If JSON parsing fails, try string matching
                    if target_state in str(version.data):
                        return get_datetime(version.creation)
        
        # Method 2: Check Comment table for workflow actions
        comment_data = frappe.db.sql("""
            SELECT creation, content
            FROM `tabComment`
            WHERE reference_doctype = %s
                AND reference_name = %s
                AND comment_type = 'Workflow'
            ORDER BY creation ASC
        """, (doctype, docname), as_dict=1)
        
        for comment in comment_data:
            if target_state in str(comment.content):
                return get_datetime(comment.creation)
        
        # Method 3: If workflow state matches current state, use modified time
        doc = frappe.get_doc(doctype, docname)
        if hasattr(doc, 'workflow_state') and doc.workflow_state == target_state:
            return get_datetime(doc.modified)
            
    except Exception as e:
        frappe.log_error(f"Error getting workflow state timestamp for {docname}: {str(e)}")
    
    return None

def get_mr_workflow_times(mr_no):
    """
    Get workflow transition times for Material Request
    Returns: {
        'approved_time': when MR was approved (Approved From Function Head)
    }
    """
    # Get when MR was approved
    approved_time = get_workflow_state_timestamp(
        "Material Request",
        mr_no,
        "Approved From Function Head"
    )
    
    # Fallback: use modified time if approved
    if not approved_time:
        mr_doc = frappe.get_doc("Material Request", mr_no)
        if mr_doc.docstatus == 1:
            approved_time = get_datetime(mr_doc.modified)
    
    return {'approved_time': approved_time}

def get_po_workflow_times(po_no):
    """
    Get workflow transition times for Purchase Order
    Returns: {
        'draft_time': when PO was created (Draft),
        'pending_time': when PO was sent for approval (Pending Approval Of Purchase Head),
        'approved_time': when PO was approved (Approved By Purchase Head)
    }
    """
    po_doc = frappe.get_doc("Purchase Order", po_no)
    
    # Draft time = creation time
    draft_time = get_datetime(po_doc.creation)
    
    # Get when PO was sent for approval
    pending_time = get_workflow_state_timestamp(
        "Purchase Order",
        po_no,
        "Pending Approval Of Purchase Head"
    )
    
    # Get when PO was approved
    approved_time = get_workflow_state_timestamp(
        "Purchase Order",
        po_no,
        "Approved By Purchase Head"
    )
    
    # Fallback: use modified time if approved
    if not approved_time and po_doc.docstatus == 1:
        approved_time = get_datetime(po_doc.modified)
    
    return {
        'draft_time': draft_time,
        'pending_time': pending_time,
        'approved_time': approved_time
    }

def get_pi_workflow_times(pi_no):
    """
    Get workflow transition times for Purchase Invoice
    Returns: {
        'pending_time': when PI was sent for approval,
        'approved_time': when PI was approved
    }
    """
    pi_doc = frappe.get_doc("Purchase Invoice", pi_no)
    
    # Get when PI was sent for approval
    pending_time = get_workflow_state_timestamp(
        "Purchase Invoice",
        pi_no,
        "Pending by Accounts Manager"
    )
    
    # Get when PI was approved
    approved_time = get_workflow_state_timestamp(
        "Purchase Invoice",
        pi_no,
        "Approved By Account Manager"
    )
    
    # Fallback: use modified time if approved
    if not approved_time and pi_doc.docstatus == 1:
        approved_time = get_datetime(pi_doc.modified)
    
    return {
        'pending_time': pending_time,
        'approved_time': approved_time
    }

def get_data(filters):
    """Fetch and process data"""
    conditions = get_conditions(filters)
    
    # Main query to get Material Request items
    query = """
        SELECT
            mri.parent as mr_no,
            mr.creation AS mr_creation,
            mr.schedule_date AS schedule_date,
            mri.item_code,
            mri.item_name,
            mri.qty as required_qty,
            mr.status as mr_status,
            mr.workflow_state as mr_workflow_state
        FROM
            `tabMaterial Request Item` mri
        INNER JOIN
            `tabMaterial Request` mr ON mri.parent = mr.name
        WHERE
            mr.docstatus = 1
            {conditions}
        ORDER BY
            mr.creation DESC, mr.name
    """.format(conditions=conditions)
    
    mr_data = frappe.db.sql(query, filters, as_dict=1)
    
    data = []
    sno = 1
    
    for mr_item in mr_data:
        # Get MR workflow times
        mr_times = get_mr_workflow_times(mr_item.mr_no)
        mr_approved_time = mr_times['approved_time']
        
        # Get Purchase Order details
        po_details = get_purchase_order_details(mr_item.mr_no, mr_item.item_code)
        
        if po_details:
            for po in po_details:
                # Get PO workflow times
                po_times = get_po_workflow_times(po.po_no)
                po_draft_time = po_times['draft_time']
                po_pending_time = po_times['pending_time']
                po_approved_time = po_times['approved_time']
                
                # Get Purchase Receipt (GRN) details
                grn_details = get_grn_details(po.po_no, mr_item.item_code)
                grn_time = get_datetime(grn_details.get('grn_datetime')) if grn_details.get('grn_datetime') else None
                
                # Get Purchase Invoice details
                pi_details = get_purchase_invoice_details(po.po_no, mr_item.item_code)
                
                pi_approved_time = None
                if pi_details.get('invoice_no'):
                    pi_times = get_pi_workflow_times(pi_details['invoice_no'])
                    pi_approved_time = pi_times['approved_time']
                
                # Calculate time differences in seconds
                mr_to_pr_seconds = None
                pr_to_po_seconds = None
                po_to_grn_seconds = None
                grn_to_pi_seconds = None
                total_seconds = None
                
                # MR → PR: From MR approved to PO draft creation
                if mr_approved_time and po_draft_time:
                    mr_to_pr_seconds = time_diff_in_seconds(po_draft_time, mr_approved_time)
                
                # PR → PO: From PO draft to PO approved
                if po_draft_time and po_approved_time:
                    # Use pending time if available, otherwise use approved time
                    if po_pending_time:
                        pr_to_po_seconds = time_diff_in_seconds(po_approved_time, po_pending_time)
                    else:
                        pr_to_po_seconds = time_diff_in_seconds(po_approved_time, po_draft_time)
                
                # PO → GRN: From PO approved to GRN
                if po_approved_time and grn_time:
                    po_to_grn_seconds = time_diff_in_seconds(grn_time, po_approved_time)
                
                # GRN → PI: From GRN to PI approved
                if grn_time and pi_approved_time:
                    grn_to_pi_seconds = time_diff_in_seconds(pi_approved_time, grn_time)
                
                # Total Lead Time: From MR approved to PI approved
                if mr_approved_time and pi_approved_time:
                    total_seconds = time_diff_in_seconds(pi_approved_time, mr_approved_time)
                
                remaining_qty = flt(po.ordered_qty) - flt(grn_details.get('received_qty', 0))
                
                row = {
                    "sno": sno,
                    "mr_no": mr_item.mr_no,
                    "mr_date": mr_approved_time,
                    "schedule_date": mr_item.schedule_date,
                    "item_code": mr_item.item_code,
                    "item_name": mr_item.item_name,
                    "required_qty": mr_item.required_qty,
                    "pr_no": po.po_no,
                    "pr_date": po_draft_time,
                    "po_no": po.po_no,
                    "po_date": po_approved_time,
                    "vendor_name": po.supplier,
                    "ordered_qty": po.ordered_qty,
                    "received_qty": grn_details.get('received_qty', 0),
                    "remaining_qty": remaining_qty,
                    "invoice_no": pi_details.get('invoice_no'),
                    "invoice_date": pi_approved_time,
                    "mr_to_pr_time": format_time_difference(mr_to_pr_seconds),
                    "pr_to_po_time": format_time_difference(pr_to_po_seconds),
                    "po_to_grn_time": format_time_difference(po_to_grn_seconds),
                    "grn_to_pi_time": format_time_difference(grn_to_pi_seconds),
                    "total_lead_time": format_time_difference(total_seconds),
                    "rate": po.rate,
                    "po_value": po.amount,
                    "invoice_amount": pi_details.get('invoice_amount', 0),
                    "mr_status": mr_item.mr_status,
                    "po_status": po.status,
                    "invoice_status": pi_details.get('invoice_status', 'Not Created')
                }
                
                data.append(row)
                sno += 1
        else:
            # No PO created yet
            row = {
                "sno": sno,
                "mr_no": mr_item.mr_no,
                "mr_date": mr_approved_time,
                "schedule_date": mr_item.schedule_date,
                "item_code": mr_item.item_code,
                "item_name": mr_item.item_name,
                "required_qty": mr_item.required_qty,
                "mr_status": mr_item.mr_status,
                "po_status": "Not Created"
            }
            data.append(row)
            sno += 1
    
    return data

def get_conditions(filters):
    """Build filter conditions"""
    conditions = ""
    
    if filters.get("from_date"):
        conditions += " AND mr.creation >= %(from_date)s"
    
    if filters.get("to_date"):
        conditions += " AND mr.creation <= %(to_date)s"
    
    if filters.get("material_request"):
        conditions += " AND mr.name = %(material_request)s"
    
    if filters.get("item_code"):
        conditions += " AND mri.item_code = %(item_code)s"
    
    if filters.get("supplier"):
        conditions += " AND EXISTS (SELECT 1 FROM `tabPurchase Order` po INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent WHERE poi.material_request = mr.name AND po.supplier = %(supplier)s)"
    
    return conditions

def get_purchase_order_details(mr_no, item_code):
    """Get Purchase Order details"""
    po_data = frappe.db.sql("""
        SELECT
            po.name as po_no,
            po.creation as po_creation,
            po.supplier,
            po.status,
            po.workflow_state,
            poi.qty as ordered_qty,
            poi.rate,
            poi.amount
        FROM
            `tabPurchase Order` po
        INNER JOIN
            `tabPurchase Order Item` poi ON po.name = poi.parent
        WHERE
            po.docstatus = 1
            AND poi.material_request = %s
            AND poi.item_code = %s
        ORDER BY
            po.creation DESC
    """, (mr_no, item_code), as_dict=1)
    
    return po_data

def get_grn_details(po_no, item_code):
    """Get Purchase Receipt (GRN) details"""
    grn_data = frappe.db.sql("""
        SELECT
            SUM(pri.qty) as received_qty,
            MAX(pr.posting_date) as grn_date,
            MAX(pr.modified) as grn_datetime
        FROM
            `tabPurchase Receipt` pr
        INNER JOIN
            `tabPurchase Receipt Item` pri ON pr.name = pri.parent
        WHERE
            pr.docstatus = 1
            AND pri.purchase_order = %s
            AND pri.item_code = %s
    """, (po_no, item_code), as_dict=1)
    
    return grn_data[0] if grn_data else {}

def get_purchase_invoice_details(po_no, item_code):
    """Get Purchase Invoice details"""
    pi_data = frappe.db.sql("""
        SELECT
            pi.name as invoice_no,
            pi.posting_date as invoice_date,
            pi.modified as invoice_datetime,
            SUM(pii.amount) as invoice_amount,
            pi.status as invoice_status
        FROM
            `tabPurchase Invoice` pi
        INNER JOIN
            `tabPurchase Invoice Item` pii ON pi.name = pii.parent
        WHERE
            pi.docstatus = 1
            AND pii.purchase_order = %s
            AND pii.item_code = %s
        GROUP BY
            pi.name
        ORDER BY
            pi.posting_date DESC
        LIMIT 1
    """, (po_no, item_code), as_dict=1)
    
    return pi_data[0] if pi_data else {}