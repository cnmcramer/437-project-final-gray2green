"""
app/services/calendar_service.py
Google Calendar API — appointment event creation.
"""

import os
from datetime import datetime, timedelta

CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID', 'cnelsoncramer@gmail.com')
SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')

SCOPES = ['https://www.googleapis.com/auth/calendar']

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    calendar_service = build('calendar', 'v3', credentials=credentials)
    CALENDAR_AVAILABLE = True
except Exception as e:
    print(f"[Calendar] Not available (likely local dev): {e}")
    calendar_service = None
    CALENDAR_AVAILABLE = False


def create_appointment_event(appointment: dict) -> str:
    """
    Create a Google Calendar event for an appointment.
    Returns the event ID, or a placeholder if Calendar is not configured.

    appointment dict fields:
        fullName, phone, email, address,
        serviceId, appointmentDate (YYYY-MM-DD),
        appointmentTime (e.g. '10:00 AM'), notes
    """
    if not CALENDAR_AVAILABLE:
        print(f"[Calendar] Skipping event creation for: {appointment.get('fullName')}")
        return "local-dev-event-id"

    # Parse date + time
    date_str = appointment.get('appointmentDate', '')
    time_str = appointment.get('appointmentTime', '9:00 AM')

    try:
        dt_start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        dt_start = datetime.strptime(date_str, "%Y-%m-%d")

    dt_end = dt_start + timedelta(hours=2)  # Default 2-hour block

    service_label = appointment.get('serviceId', 'Service').replace('-', ' ').title()
    summary = f"Gray to Green — {service_label} for {appointment.get('fullName', 'Client')}"

    description_lines = [
        f"Client: {appointment.get('fullName', '')}",
        f"Phone: {appointment.get('phone', '')}",
        f"Email: {appointment.get('email', '')}",
        f"Address: {appointment.get('address', '')}",
        f"Service: {service_label}",
    ]
    if appointment.get('notes'):
        description_lines.append(f"Notes: {appointment['notes']}")

    event_body = {
        'summary': summary,
        'description': '\n'.join(description_lines),
        'location': appointment.get('address', ''),
        'start': {
            'dateTime': dt_start.isoformat(),
            'timeZone': 'America/Detroit',
        },
        'end': {
            'dateTime': dt_end.isoformat(),
            'timeZone': 'America/Detroit',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }

    event = calendar_service.events().insert(
        calendarId=CALENDAR_ID,
        body=event_body
    ).execute()

    return event.get('id', '')
