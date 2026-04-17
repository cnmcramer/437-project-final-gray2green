"""
app/routes/services.py
GET /api/services
"""

from flask import Blueprint, jsonify
from app.services.firestore_service import get_all_services

services_bp = Blueprint('services', __name__)


@services_bp.route('/api/services', methods=['GET'])
def get_services():
    try:
        services = get_all_services()
        return jsonify({
            'success': True,
            'message': 'Services retrieved successfully.',
            'services': services,
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to retrieve services: {str(e)}',
        }), 500
