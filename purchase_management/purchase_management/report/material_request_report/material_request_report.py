import frappe
from frappe import _
from frappe.utils import flt, get_datetime, time_diff_in_seconds
import json

# ---------------------------------------------------------------------
# Main Report Entry
# ---------------------------------------------------------------------

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    # Pagination
    page_length = 50
    start = filters.get("start", 0) or 0
    total_records = len(data)
    paginated_data = data[start:start + page_length]

    report_summary = []
    if total_records > page_length:
        current_page = (start // page_length) + 1
        total_pages = (total_records + page_length - 1) // page_length
        report_summary.append({
            "value": f"Page {current_page} of {total_pages}",
            "indicator": "blue",
            "label": f"Showing records {start + 1}–{min(start + page_length, total_records)} of {total_records}"
        })

    return columns, paginated_data, None, None, report_summary


# ---------------------------------------------------------------------
# Columns
# ---------------------------------------------------------------------

def get_columns():
    return [
        {"fieldname": "mr_no", "label": _("MR No."), "fieldtype": "Link", "options": "Material Request", "width": 150},
        {"fieldname": "mr_date", "label": _("MR Date"), "fieldtype": "Datetime", "width": 150},
        {"fieldname": "schedule_date", "label": _("Requested By / Dept."), "fieldtype": "Data", "width": 150},
        {"fieldname": "item_code", "label": _("Item Code"), "fieldtype": "Link", "options": "Item", "width": 120},
        {"fieldname": "item_name", "label": _("Item Name"), "fieldtype": "Data", "width": 180},
        {"fieldname": "required_qty", "label": _("Required Qty"), "fieldtype": "Float", "width": 100},
        {"fieldname": "po_no", "label": _("PO No."), "fieldtype": "Link", "options": "Purchase Order", "width": 150},
        {"fieldname": "po_date", "label": _("PO Date"), "fieldtype": "Datetime", "width": 150},
        {"fieldname": "vendor_name", "label": _("Vendor Name"), "fieldtype": "Link", "options": "Supplier", "width": 150},
        {"fieldname": "ordered_qty", "label": _("Ordered Qty"), "fieldtype": "Float", "width": 100},
        {"fieldname": "received_qty", "label": _("Received Qty (GRN)"), "fieldtype": "Float", "width": 120},
        {"fieldname": "remaining_qty", "label": _("Remaining Qty"), "fieldtype": "Float", "width": 100},
        {"fieldname": "invoice_no", "label": _("Invoice No."), "fieldtype": "Link", "options": "Purchase Invoice", "width": 150},
        {"fieldname": "invoice_date", "label": _("Invoice Date"), "fieldtype": "Datetime", "width": 150},

        # Lead Times
        {"fieldname": "mr_to_po_time", "label": _("MR → PO"), "fieldtype": "Data", "width": 120},
        {"fieldname": "mr_to_grn_time", "label": _("MR → GRN"), "fieldtype": "Data", "width": 120},
        {"fieldname": "po_to_grn_time", "label": _("PO → GRN"), "fieldtype": "Data", "width": 120},
        {"fieldname": "grn_to_pi_time", "label": _("GRN → PI"), "fieldtype": "Data", "width": 120},
        {"fieldname": "total_lead_time", "label": _("Total Lead Time"), "fieldtype": "Data", "width": 150},
        {"fieldname": "lead_time_days", "label": _("Lead Time From Item"), "fieldtype": "Data", "width": 150},
        {"fieldname": "rate", "label": _("Rate / Unit"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "po_value", "label": _("PO Value (₹)"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "invoice_amount", "label": _("Invoice Amount (₹)"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "mr_status", "label": _("MR Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "po_status", "label": _("PO Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "invoice_status", "label": _("Invoice Status"), "fieldtype": "Data", "width": 120}
    ]


# ---------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------

def format_time_difference(seconds):
    if not seconds or seconds < 0:
        return ""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days >= 1:
        return f"{int(days)}d {int(hours)}h" if hours else f"{int(days)} days"
    elif hours >= 1:
        return f"{int(hours)}h {int(minutes)}m" if minutes else f"{int(hours)} hrs"
    elif minutes >= 1:
        return f"{int(minutes)} mins"
    return "< 1 min"


def get_workflow_state_timestamp(doctype, docname, target_state):
    try:
        version_data = frappe.db.sql("""
            SELECT creation, data FROM `tabVersion`
            WHERE ref_doctype=%s AND docname=%s ORDER BY creation ASC
        """, (doctype, docname), as_dict=1)
        for v in version_data:
            if v.data:
                try:
                    data = json.loads(v.data)
                    if data.get("changed"):
                        for c in data["changed"]:
                            if c[0] == "workflow_state" and len(c) > 2 and c[2] == target_state:
                                return get_datetime(v.creation)
                except:
                    if target_state in str(v.data):
                        return get_datetime(v.creation)

        comment_data = frappe.db.sql("""
            SELECT creation, content FROM `tabComment`
            WHERE reference_doctype=%s AND reference_name=%s AND comment_type='Workflow'
        """, (doctype, docname), as_dict=1)
        for c in comment_data:
            if target_state in str(c.content):
                return get_datetime(c.creation)

        doc = frappe.get_doc(doctype, docname)
        if getattr(doc, "workflow_state", None) == target_state:
            return get_datetime(doc.modified)
    except Exception as e:
        frappe.log_error(f"Error getting workflow state timestamp for {docname}: {str(e)}")
    return None


# ---------------------------------------------------------------------
# Workflow Time Fetchers
# ---------------------------------------------------------------------

def get_mr_workflow_times(mr_no):
    approved_time = get_workflow_state_timestamp("Material Request", mr_no, "Approved From Function Head")
    if not approved_time:
        mr_doc = frappe.get_doc("Material Request", mr_no)
        if mr_doc.docstatus == 1:
            approved_time = get_datetime(mr_doc.modified)
    return {"approved_time": approved_time}


def get_po_workflow_times(po_no):
    po_doc = frappe.get_doc("Purchase Order", po_no)
    draft_time = get_datetime(po_doc.creation)
    approved_time = get_workflow_state_timestamp("Purchase Order", po_no, "Approved By Purchase Head")
    if not approved_time and po_doc.docstatus == 1:
        approved_time = get_datetime(po_doc.modified)
    return {"draft_time": draft_time, "approved_time": approved_time}


def get_pi_workflow_times(pi_no):
    pi_doc = frappe.get_doc("Purchase Invoice", pi_no)
    approved_time = get_workflow_state_timestamp("Purchase Invoice", pi_no, "Approved By Account Manager")
    if not approved_time and pi_doc.docstatus == 1:
        approved_time = get_datetime(pi_doc.modified)
    return {"approved_time": approved_time}


# ---------------------------------------------------------------------
# Data Query and Lead Time Calculations
# ---------------------------------------------------------------------

def get_data(filters):
    conditions = get_conditions(filters)

    # Excluded item creation types - Capex/Asset items should never show in this report
    excluded_creation_types = ("R&D-Capex/Asset", "Capex/Asset")

    mr_query = f"""
        SELECT
            mri.parent AS mr_no,
            mr.creation AS mr_creation,
            mr.schedule_date AS schedule_date,
            mri.item_code, mri.item_name, mri.qty AS required_qty,
            mr.status AS mr_status,
            item.lead_time_days AS lead_time_days
        FROM `tabMaterial Request Item` mri
        INNER JOIN `tabMaterial Request` mr ON mri.parent = mr.name
        LEFT JOIN `tabItem` item ON item.name = mri.item_code
        WHERE mr.docstatus = 1
            AND mr.material_request_type = 'Purchase'
            AND (item.custom_item_creation_type IS NULL OR item.custom_item_creation_type NOT IN %(excluded_creation_types)s)
            {conditions}
        ORDER BY mr.creation DESC, mr.name, mri.idx
    """

    sql_params = dict(filters)
    sql_params["excluded_creation_types"] = excluded_creation_types

    mr_data = frappe.db.sql(mr_query, sql_params, as_dict=1)

    data, sno, prev_mr_no = [], 1, None
    for mr_item in mr_data:
        mr_no = mr_item.mr_no
        is_first_item = (mr_no != prev_mr_no)
        mr_times = get_mr_workflow_times(mr_no)
        mr_approved_time = mr_times["approved_time"]

        po_details = get_purchase_order_details(mr_no, mr_item.item_code)
        if po_details:
            for po in po_details:
                po_times = get_po_workflow_times(po.po_no)
                po_approved_time = po_times["approved_time"]

                grn = get_grn_details(po.po_no, mr_item.item_code)
                grn_time = get_datetime(grn.get("grn_datetime")) if grn.get("grn_datetime") else None

                pi = get_purchase_invoice_details(po.po_no, mr_item.item_code)
                pi_approved_time = None
                if pi.get("invoice_no"):
                    pi_times = get_pi_workflow_times(pi["invoice_no"])
                    pi_approved_time = pi_times["approved_time"]

                # Lead Time Calculation
                mr_to_po_seconds = mr_to_grn_seconds = po_to_grn_seconds = grn_to_pi_seconds = total_seconds = None
                if mr_approved_time and po_approved_time:
                    mr_to_po_seconds = time_diff_in_seconds(po_approved_time, mr_approved_time)
                if mr_approved_time and grn_time:
                    mr_to_grn_seconds = time_diff_in_seconds(grn_time, mr_approved_time)
                if po_approved_time and grn_time:
                    po_to_grn_seconds = time_diff_in_seconds(grn_time, po_approved_time)
                if grn_time and pi_approved_time:
                    grn_to_pi_seconds = time_diff_in_seconds(pi_approved_time, grn_time)
                if mr_approved_time and pi_approved_time:
                    total_seconds = time_diff_in_seconds(pi_approved_time, mr_approved_time)

                remaining_qty = flt(po.ordered_qty) - flt(grn.get("received_qty", 0))

                data.append({
                    "sno": sno if is_first_item else "",
                    "mr_no": mr_no if is_first_item else "",
                    "mr_date": mr_approved_time if is_first_item else "",
                    "schedule_date": mr_item.schedule_date if is_first_item else "",
                    "item_code": mr_item.item_code,
                    "item_name": mr_item.item_name,
                    "required_qty": mr_item.required_qty,
                    "po_no": po.po_no,
                    "po_date": po_approved_time,
                    "vendor_name": po.supplier,
                    "ordered_qty": po.ordered_qty,
                    "received_qty": grn.get("received_qty", 0),
                    "remaining_qty": remaining_qty,
                    "invoice_no": pi.get("invoice_no"),
                    "invoice_date": pi_approved_time,
                    "mr_to_po_time": format_time_difference(mr_to_po_seconds),
                    "mr_to_grn_time": format_time_difference(mr_to_grn_seconds),
                    "po_to_grn_time": format_time_difference(po_to_grn_seconds),
                    "grn_to_pi_time": format_time_difference(grn_to_pi_seconds),
                    "total_lead_time": format_time_difference(total_seconds),
                    "lead_time_days": mr_item.lead_time_days,
                    "rate": po.rate,
                    "po_value": po.amount,
                    "invoice_amount": pi.get("invoice_amount", 0),
                    "mr_status": mr_item.mr_status if is_first_item else "",
                    "po_status": po.status,
                    "invoice_status": pi.get("invoice_status", "Not Created"),
                })
            sno += 1
        else:
            data.append({
                "sno": sno,
                "mr_no": mr_no,
                "mr_date": mr_approved_time,
                "schedule_date": mr_item.schedule_date,
                "item_code": mr_item.item_code,
                "item_name": mr_item.item_name,
                "required_qty": mr_item.required_qty,
                "lead_time_days": mr_item.lead_time_days,
                "mr_status": mr_item.mr_status,
                "po_status": "Not Created"
            })
            sno += 1
        prev_mr_no = mr_no
    return data


# ---------------------------------------------------------------------
# Query Conditions and Helpers
# ---------------------------------------------------------------------

def get_conditions(filters):
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
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabPurchase Order` po
            INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
            WHERE poi.material_request = mr.name AND po.supplier = %(supplier)s
        )"""
    if filters.get("purchase_order"):
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabPurchase Order` po
            INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
            WHERE poi.material_request = mr.name AND po.name = %(purchase_order)s
        )"""
    if filters.get("purchase_invoice"):
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabPurchase Invoice` pi
            INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
            WHERE pii.item_code = mri.item_code AND pii.purchase_order IN (
                SELECT po.name FROM `tabPurchase Order` po
                INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
                WHERE poi.material_request = mr.name
            ) AND pi.name = %(purchase_invoice)s
        )"""
    return conditions


def get_purchase_order_details(mr_no, item_code):
    return frappe.db.sql("""
        SELECT po.name AS po_no, po.creation, po.supplier, po.status,
               poi.qty AS ordered_qty, poi.rate, poi.amount
        FROM `tabPurchase Order` po
        INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
        WHERE po.docstatus = 1 AND poi.material_request = %s AND poi.item_code = %s
        ORDER BY po.creation DESC
    """, (mr_no, item_code), as_dict=1)


def get_grn_details(po_no, item_code):
    res = frappe.db.sql("""
        SELECT SUM(pri.qty) AS received_qty, MAX(pr.modified) AS grn_datetime
        FROM `tabPurchase Receipt` pr
        INNER JOIN `tabPurchase Receipt Item` pri ON pr.name = pri.parent
        WHERE pr.docstatus = 1 AND pri.purchase_order = %s AND pri.item_code = %s
    """, (po_no, item_code), as_dict=1)
    return res[0] if res else {}


def get_purchase_invoice_details(po_no, item_code):
    res = frappe.db.sql("""
        SELECT pi.name AS invoice_no, pi.modified AS invoice_datetime,
               SUM(pii.amount) AS invoice_amount, pi.status AS invoice_status
        FROM `tabPurchase Invoice` pi
        INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
        WHERE pi.docstatus = 1 AND pii.purchase_order = %s AND pii.item_code = %s
        GROUP BY pi.name ORDER BY pi.posting_date DESC LIMIT 1
    """, (po_no, item_code), as_dict=1)
    return res[0] if res else {}