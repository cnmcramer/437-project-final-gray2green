"""
app/routes/appointments.py
POST /api/appointments
"""

from flask import Blueprint, request, jsonify
from app.services.firestore_service import save_appointment, update_appointment_event_id
from app.services.calendar_service import create_appointment_event

appointments_bp = Blueprint('appointments', __name__)

REQUIRED_FIELDS = ['fullName', 'phone', 'serviceId', 'appointmentDate']


@appointments_bp.route('/api/appointments', methods=['POST'])
def submit_appointment():
    try:
        data = request.get_json(silent=True) or {}

        # ── Validate ───────────────────────────────────────────────────
        missing = [f for f in REQUIRED_FIELDS if not data.get(f, '').strip()]
        if missing:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing)}',
            }), 400

        # ── Save to Firestore ──────────────────────────────────────────
        doc_id = save_appointment(data)

        # ── Create Google Calendar event ───────────────────────────────
        event_id = None
        try:
            event_id = create_appointment_event(data)
            if doc_id and event_id:
                update_appointment_event_id(doc_id, event_id)
        except Exception as cal_err:
            # Calendar failure should NOT block the appointment being saved
            print(f"[Calendar] Event creation failed (non-fatal): {cal_err}")

        return jsonify({
            'success': True,
            'message': "Appointment requested! We'll confirm shortly.",
            'id': doc_id,
            'calendarEventId': event_id,
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}',
        }), 500
