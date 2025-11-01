import frappe

class SavingsService:
    @staticmethod
    def get_member_savings_summary(member):
        total_savings = frappe.db.sql("""
            SELECT SUM(amount) FROM `tabSavings Contribution` 
            WHERE member = %s AND contribution_type = 'Regular'
        """, member)[0][0] or 0
        
        return {
            "total_savings": total_savings,
            "last_contribution_date": frappe.db.get_value("Savings Contribution", 
                {"member": member}, "contribution_date", order_by="contribution_date desc")
        }
