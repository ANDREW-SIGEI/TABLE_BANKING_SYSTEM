import frappe
from tablebanking.backend.loan_service import LoanService

@frappe.whitelist(allow_guest=False)
def apply_loan(member, loan_type, amount, duration):
    try:
        loan_app = frappe.get_doc({
            "doctype": "Loan Application",
            "member": member,
            "loan_type": loan_type,
            "loan_amount": amount,
            "duration_months": duration,
            "status": "Pending"
        })
        loan_app.insert()
        
        return {"success": True, "loan_id": loan_app.name}
    except Exception as e:
        return {"success": False, "message": str(e)}

@frappe.whitelist(allow_guest=False)
def get_loan_calculations(loan_type, principal, duration, interest_rate):
    try:
        if loan_type == "Short Term":
            calculations = LoanService.calculate_short_term_loan(
                principal, interest_rate, duration
            )
        elif loan_type == "Long Term":
            calculations = LoanService.calculate_long_term_loan(
                principal, interest_rate, duration
            )
        else:
            return {"success": False, "message": "Invalid loan type"}
        
        return {"success": True, "calculations": calculations}
    except Exception as e:
        return {"success": False, "message": str(e)}
