"""
app/services/calendar_service.py
Google Calendar API — appointment event creation.
"""

import os
from datetime import datetime, timedelta

CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID', 'cnelsoncramer@gmail.com')
SCOPES = ['https://www.googleapis.com/auth/calendar']

try:
    import google.auth
    from googleapiclient.discovery import build

    credentials, project = google.auth.default(scopes=SCOPES)
    calendar_service = build('calendar', 'v3', credentials=credentials)
    CALENDAR_AVAILABLE = True
    print("[Calendar] Connected successfully")
except Exception as e:
    print(f"[Calendar] Not available: {e}")
    calendar_service = None
    CALENDAR_AVAILABLE = False


def create_appointment_event(appointment: dict) -> str:
    if not CALENDAR_AVAILABLE:
        print(f"[Calendar] Skipping event creation for: {appointment.get('fullName')}")
        return "local-dev-event-id"

    # Parse date + time
    date_str = appointment.get('appointmentDate') or appointment.get('preferredDate', '')
    time_str = appointment.get('appointmentTime', '9:00 AM')

    # If no date provided, default to tomorrows

    if not date_str:
        date_str = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

    try:
        dt_start = datetime.strptime(f"{date_str} {time_str}".strip(), "%Y-%m-%d %I:%M %p")
    except ValueError:
        try:
            dt_start = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            dt_start = datetime.utcnow()

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
