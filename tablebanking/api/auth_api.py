import frappe
from tablebanking.backend.jwt_auth import JWTAuth

@frappe.whitelist(allow_guest=True)
def login(phone, password):
    try:
        user = frappe.get_all("User",
            filters={"phone": phone, "enabled": 1},
            fields=["name", "first_name", "last_name"]
        )
        
        if not user:
            return {"success": False, "message": "Invalid credentials"}
        
        user = user[0]
        user_doc = frappe.get_doc("User", user.name)
        
        if not user_doc.check_password(password):
            return {"success": False, "message": "Invalid credentials"}
        
        jwt_auth = JWTAuth()
        access_token = jwt_auth.create_access_token(data={"sub": user.name})
        
        return {
            "success": True,
            "access_token": access_token,
            "user": user
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
