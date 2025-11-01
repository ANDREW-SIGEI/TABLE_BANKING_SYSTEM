import frappe
from frappe import _

class LoanService:
    @staticmethod
    def calculate_short_term_loan(principal, interest_rate, duration_months):
        if duration_months > 3:
            frappe.throw(_("Short-term loans must be 3 months or less"))
        
        total_interest = principal * (interest_rate / 100)
        total_amount = principal + total_interest
        monthly_installment = total_amount / duration_months
        
        return {
            "principal": principal,
            "total_interest": total_interest,
            "total_amount": total_amount,
            "monthly_installment": monthly_installment
        }
    
    @staticmethod
    def calculate_long_term_loan(principal, annual_interest_rate, duration_months, key_in_box=0):
        monthly_interest_rate = annual_interest_rate / 12 / 100
        schedule = []
        remaining_balance = principal
        
        for month in range(1, duration_months + 1):
            monthly_interest = remaining_balance * monthly_interest_rate
            principal_component = (principal / duration_months) + key_in_box
            total_payment = principal_component + monthly_interest
            
            if remaining_balance < principal_component:
                principal_component = remaining_balance
                total_payment = principal_component + monthly_interest
            
            remaining_balance -= principal_component
            
            schedule.append({
                "month": month,
                "principal_component": principal_component,
                "interest_component": monthly_interest,
                "total_payment": total_payment,
                "remaining_balance": remaining_balance
            })
        
        return schedule
