import frappe

@frappe.whitelist(allow_guest=False)
def track_location(latitude, longitude):
    try:
        # This would record officer location in database
        return {"success": True, "message": "Location recorded"}
    except Exception as e:
        return {"success": False, "message": str(e)}
