from frappe import _

def get_data():
    return [
        {
            "module_name": "Table Banking",
            "type": "module",
            "label": _("Table Banking")
        },
        {
            "type": "page",
            "name": "dashboard",
            "label": _("Dashboard"),
            "icon": "fa fa-dashboard"
        },
        {
            "type": "page", 
            "name": "groups",
            "label": _("Groups"),
            "icon": "fa fa-users"
        },
        {
            "type": "page",
            "name": "members", 
            "label": _("Members"),
            "icon": "fa fa-user"
        },
        {
            "type": "page",
            "name": "loans",
            "label": _("Loans"),
            "icon": "fa fa-money"
        }
    ]
