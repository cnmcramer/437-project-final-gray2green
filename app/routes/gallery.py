"""
app/routes/gallery.py
GET /api/gallery
"""

from flask import Blueprint, jsonify
from app.services.firestore_service import get_gallery_images

gallery_bp = Blueprint('gallery', __name__)


@gallery_bp.route('/api/gallery', methods=['GET'])
def get_gallery():
    try:
        images = get_gallery_images()
        return jsonify({
            'success': True,
            'message': 'Gallery retrieved successfully.',
            'images': images,
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to retrieve gallery: {str(e)}',
        }), 500
