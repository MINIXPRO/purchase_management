# Copyright (c) 2025, Pragati Dike and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.utils import nowdate, getdate


def execute(filters=None):
    columns, max_visits = get_columns()
    data = get_data(max_visits)
    return columns, data


def get_columns():
    columns = [
        {
            "label": "AMC ID",
            "fieldname": "amc_id",
            "fieldtype": "Link",
            "options": "AMC Equipment",
            "width": 180,
        },
        {
            "label": "Equipment No",
            "fieldname": "equipment_no",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Equipment Name",
            "fieldname": "equipment_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Location",
            "fieldname": "location",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150,
        },
		{
			"label":"Periodic Validation Scheduled Date",
			"fieldname":"periodic_validation_scheduled_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": "Periodic Validation Done Date",
			"fieldname": "periodic_validation_done_date",
			"fieldtype": "Date",
			"width": 120,
		},
    ]

    # 🔥 Find maximum visits per AMC
    max_visits = frappe.db.sql("""
        SELECT MAX(cnt) FROM (
            SELECT COUNT(*) AS cnt
            FROM `tabScheduled Log`
            GROUP BY parent
        ) t
    """)[0][0] or 0

    # 🔥 Dynamic visit columns
    for i in range(1, max_visits + 1):
        columns.extend([
            {
                "label": f"Visit-{i} No",
                "fieldname": f"visit_{i}_no",
                "fieldtype": "Data",
                "width": 100,
            },
            {
                "label": f"Visit-{i} Scheduled Date",
                "fieldname": f"visit_{i}_scheduled_date",
                "fieldtype": "Date",
                "width": 120,
            },
            {
                "label": f"Visit-{i} Done Date",
                "fieldname": f"visit_{i}_done_date",
                "fieldtype": "Date",
                "width": 120,
            },
            {
                "label": f"Visit-{i} Activity Type",
                "fieldname": f"visit_{i}_activity",
                "fieldtype": "Data",
                "width": 150,
            },
            {
                "label": f"Visit-{i} Status",
                "fieldname": f"visit_{i}_status",
                "fieldtype": "Data",
                "width": 100,
            },
        ])

    return columns, max_visits


def get_data(max_visits):
    data = []

    amc_list = frappe.db.sql("""
        SELECT
            name,
            equipment_no,
            equipment_name,
            location,
			periodic_validation_scheduled_date,
			periodic_validation_done_date
        FROM `tabAMC Equipment`
        ORDER BY name
    """, as_dict=True)

    today = getdate(nowdate())

    for amc in amc_list:
        row = {
            "amc_id": amc.name,
            "equipment_no": amc.equipment_no,
            "equipment_name": amc.equipment_name,
            "location": amc.location,
			"periodic_validation_scheduled_date" : amc.periodic_validation_scheduled_date,
			"periodic_validation_done_date" : amc.periodic_validation_done_date,
        }

        visits = frappe.db.sql("""
            SELECT
                visit_no,
                scheduled_date,
                done_date,
                activity_type
            FROM `tabScheduled Log`
            WHERE parent = %s
            ORDER BY scheduled_date
        """, amc.name, as_dict=True)

        for idx, visit in enumerate(visits, start=1):
            if idx > max_visits:
                break

            scheduled_date = getdate(visit.scheduled_date) if visit.scheduled_date else None
            done_date = getdate(visit.done_date) if visit.done_date else None

            if done_date:
                status = "Completed"
            elif scheduled_date and scheduled_date < today:
                status = "Overdue"
            else:
                status = "Upcoming"

            row[f"visit_{idx}_no"] = visit.visit_no
            row[f"visit_{idx}_scheduled_date"] = scheduled_date
            row[f"visit_{idx}_done_date"] = done_date
            row[f"visit_{idx}_activity"] = visit.activity_type
            row[f"visit_{idx}_status"] = status

        data.append(row)

    return data
