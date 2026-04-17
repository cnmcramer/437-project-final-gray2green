import os
import uuid
from datetime import datetime

BUCKET_NAME = os.environ.get('GCS_BUCKET', 'gray-to-green-uploads')

try:
    from google.cloud import storage as gcs
    storage_client = gcs.Client()
    GCS_AVAILABLE = True
except Exception as e:
    print(f"[Storage] Not available (likely local dev): {e}")
    storage_client = None
    GCS_AVAILABLE = False


def upload_image(file_obj, original_filename: str, folder: str = 'quotes') -> str:
    if not GCS_AVAILABLE:
        print(f"[Storage] Skipping upload for: {original_filename}")
        return f"https://storage.googleapis.com/{BUCKET_NAME}/{folder}/placeholder.jpg"

    ext = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else 'jpg'
    unique_name = f"{folder}/{datetime.utcnow().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}.{ext}"

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(unique_name)
    blob.upload_from_file(file_obj, content_type=f'image/{ext}')
    blob.make_public()

    return blob.public_url


def delete_image(public_url: str):
    if not GCS_AVAILABLE:
        return

    prefix = f"https://storage.googleapis.com/{BUCKET_NAME}/"
    if not public_url.startswith(prefix):
        return

    blob_name = public_url[len(prefix):]
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.delete()
