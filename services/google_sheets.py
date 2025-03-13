from datetime import datetime, timedelta
from config import settings
from gspread import service_account, Spreadsheet


def get_due_dates():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = service_account("credenciales_gsheet.json")
    sheet = client.open_by_key(settings.SHEET_ID).sheet1
    data = sheet.get(settings.RANGE_NAME)
    today = datetime.today().date()
    reminders = []

    for row in data[1:]:
        name, date_str = row
        due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if (
            due_date - timedelta(days=10) == today
            or due_date - timedelta(days=5) == today
            or due_date == today
        ):
            reminders.append(f"Recordatorio: {name} vence el {due_date}")

    return reminders
