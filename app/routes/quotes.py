"""
app/routes/quotes.py
POST /api/quotes
"""

from flask import Blueprint, request, jsonify
from app.services.firestore_service import save_quote_request
from app.services.storage_service import upload_image

quotes_bp = Blueprint('quotes', __name__)

REQUIRED_FIELDS = ['fullName', 'phone', 'email', 'serviceId']


@quotes_bp.route('/api/quotes', methods=['POST'])
def submit_quote():
    try:
        # ── Collect JSON body ──────────────────────────────────────────
        data = request.get_json(silent=True) or {}

        # Also handle multipart form (when image is attached)
        if request.content_type and 'multipart' in request.content_type:
            data = request.form.to_dict()

        # ── Validate required fields ───────────────────────────────────
        missing = [f for f in REQUIRED_FIELDS if not data.get(f, '').strip()]
        if missing:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing)}',
            }), 400

        # ── Handle image uploads (optional) ───────────────────────────
        image_urls = []
        if 'projectImages' in request.files:
            files = request.files.getlist('projectImages')
            for f in files:
                if f and f.filename:
                    url = upload_image(f, f.filename, folder='quotes')
                    image_urls.append(url)

        if image_urls:
            data['imageUrls'] = image_urls

        # ── Save to Firestore ──────────────────────────────────────────
        doc_id = save_quote_request(data)

        return jsonify({
            'success': True,
            'message': "Quote request received! We'll reach out within 24 hours.",
            'id': doc_id,
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}',
        }), 500
