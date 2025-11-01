import frappe

@frappe.whitelist(allow_guest=False)
def get_dashboard_stats():
    try:
        total_groups = frappe.db.count("Banking Group")
        total_members = frappe.db.count("Group Member")
        active_loans = frappe.db.count("Loan Application", {"status": "Approved"})
        
        return {
            "success": True,
            "stats": {
                "total_groups": total_groups,
                "total_members": total_members,
                "active_loans": active_loans
            }
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
