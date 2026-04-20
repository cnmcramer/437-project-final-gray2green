"""
app/services/firestore_service.py
Firestore database connection and helper functions.
"""

import os
from datetime import datetime

# Only import Firestore when running in a GCP environment
try:
    from google.cloud import firestore
    db = firestore.Client(project="project-final-gray2green")
    FIRESTORE_AVAILABLE = True
    print("[Firestore] Connected successfully")
except Exception as e:
    print(f"[Firestore] Not available (likely local dev): {e}")
    db = None
    FIRESTORE_AVAILABLE = False


# ─── Collections ─────────────────────────────────────────────────────────────
QUOTE_REQUESTS   = 'quoteRequests'
APPOINTMENTS     = 'appointments'
SERVICES         = 'services'
GALLERY_IMAGES   = 'galleryImages'


# ─── Quote Requests ───────────────────────────────────────────────────────────

def save_quote_request(data: dict) -> str:
    """Save a quote request to Firestore. Returns the new document ID."""
    if not FIRESTORE_AVAILABLE:
        print("[Firestore] Skipping save (not available):", data)
        return "local-dev-id"

    data['createdAt'] = datetime.utcnow()
    data['status'] = 'new'

    ref = db.collection(QUOTE_REQUESTS).document()
    ref.set(data)
    return ref.id


# ─── Appointments ─────────────────────────────────────────────────────────────

def save_appointment(data: dict) -> str:
    """Save an appointment record to Firestore. Returns the new document ID."""
    if not FIRESTORE_AVAILABLE:
        print("[Firestore] Skipping save (not available):", data)
        return "local-dev-id"

    data['createdAt'] = datetime.utcnow()
    data['status'] = 'pending'

    ref = db.collection(APPOINTMENTS).document()
    ref.set(data)
    return ref.id


def update_appointment_event_id(doc_id: str, event_id: str):
    """Store the Google Calendar event ID back on the appointment record."""
    if not FIRESTORE_AVAILABLE:
        return
    db.collection(APPOINTMENTS).document(doc_id).update({'calendarEventId': event_id})


# ─── Services ─────────────────────────────────────────────────────────────────

def get_all_services() -> list:
    """Fetch all services from Firestore. Falls back to hardcoded data if empty."""
    if not FIRESTORE_AVAILABLE:
        return _default_services()

    docs = db.collection(SERVICES).stream()
    services = [{'id': doc.id, **doc.to_dict()} for doc in docs]

    if not services:
        return _default_services()
    return services


def seed_services():
    """Seed the services collection with default data (run once)."""
    if not FIRESTORE_AVAILABLE:
        return

    batch = db.batch()
    for svc in _default_services():
        ref = db.collection(SERVICES).document(svc['id'])
        batch.set(ref, svc)
    batch.commit()
    print("[Firestore] Services seeded.")


def _default_services() -> list:
    return [
        {
            'id': 'mulch-installation',
            'name': 'Mulch Installation',
            'icon': '🍂',
            'description': 'Fresh mulch installation to protect plants, suppress weeds, and give your beds a clean, polished look.',
            'tag': 'Most Popular',
            'order': 1,
        },
        {
            'id': 'lawn-care',
            'name': 'Lawn Care & Maintenance',
            'icon': '🌿',
            'description': 'Regular mowing, edging, trimming, and seasonal maintenance to keep your lawn looking its best.',
            'tag': 'Year-Round',
            'order': 2,
        },
        {
            'id': 'landscape-design',
            'name': 'Landscape Design',
            'icon': '🏡',
            'description': 'Custom landscape planning that transforms your outdoor space into something beautiful and functional.',
            'tag': 'Custom',
            'order': 3,
        },
        {
            'id': 'hardscaping',
            'name': 'Hardscaping',
            'icon': '🪨',
            'description': 'Patios, walkways, retaining walls, and stone features that add structure and value.',
            'tag': 'Premium',
            'order': 4,
        },
        {
            'id': 'tree-shrub-trimming',
            'name': 'Tree & Shrub Trimming',
            'icon': '✂️',
            'description': 'Expert pruning and shaping to keep your trees and shrubs healthy and looking great.',
            'tag': 'Seasonal',
            'order': 5,
        },
        {
            'id': 'clean-ups',
            'name': 'Fall & Spring Clean-Ups',
            'icon': '🍁',
            'description': 'Seasonal cleanup to prep for winter or get your yard ready to shine in spring.',
            'tag': 'Seasonal',
            'order': 6,
        },
        {
            'id': 'rock-stone',
            'name': 'Rock & Stone Installation',
            'icon': '⛰️',
            'description': 'Decorative rock, river stone, and boulder placement for edging, drainage, and curb appeal.',
            'tag': 'Design',
            'order': 7,
        },
        {
            'id': 'sod-installation',
            'name': 'Sod Installation',
            'icon': '🌱',
            'description': 'Instant lush lawn with professional sod installation — prep, lay, and aftercare included.',
            'tag': 'Transform',
            'order': 8,
        },
    ]


# ─── Gallery ──────────────────────────────────────────────────────────────────

def get_gallery_images() -> list:
    """Fetch all gallery images from Firestore."""
    if not FIRESTORE_AVAILABLE:
        return []

    docs = db.collection(GALLERY_IMAGES).order_by('order').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def save_gallery_image(data: dict) -> str:
    """Save a gallery image record to Firestore."""
    if not FIRESTORE_AVAILABLE:
        return "local-dev-id"

    data['createdAt'] = datetime.utcnow()
    ref = db.collection(GALLERY_IMAGES).document()
    ref.set(data)
    return ref.id

def save_quote_request(data: dict) -> str:
    print(f"[Firestore] FIRESTORE_AVAILABLE={FIRESTORE_AVAILABLE}, db={db}")
    if not FIRESTORE_AVAILABLE:
        print("[Firestore] Skipping save (not available):", data)
        return "local-dev-id"

    try:
        data['createdAt'] = datetime.utcnow()
        data['status'] = 'new'
        ref = db.collection(QUOTE_REQUESTS).document()
        ref.set(data)
        print(f"[Firestore] Quote saved successfully: {ref.id}")
        return ref.id
    except Exception as e:
        print(f"[Firestore] ERROR saving quote: {e}")
        raise