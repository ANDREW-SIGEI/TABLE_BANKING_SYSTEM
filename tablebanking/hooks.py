from . import __version__

app_name = "tablebanking"
app_title = "Table Banking System"
app_publisher = "Your Company"
app_description = "Comprehensive Table Banking Management System"
app_email = "your.email@example.com"
app_license = "MIT"

# Desk Notifications
notification_config = "tablebanking.notifications.get_notification_config"

# Scheduled Tasks
scheduler_events = {
    "cron": {
        "0 0 * * *": [
            "tablebanking.tasks.daily_backup"
        ]
    }
}
