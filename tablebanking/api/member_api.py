import frappe

@frappe.whitelist(allow_guest=False)
def register_member(member_data):
    try:
        member = frappe.get_doc({
            "doctype": "Group Member",
            "member_name": member_data.get("member_name"),
            "id_number": member_data.get("id_number"),
            "phone": member_data.get("phone"),
            "group": member_data.get("group")
        })
        member.insert()
        
        return {"success": True, "member_id": member.name}
    except Exception as e:
        return {"success": False, "message": str(e)}
