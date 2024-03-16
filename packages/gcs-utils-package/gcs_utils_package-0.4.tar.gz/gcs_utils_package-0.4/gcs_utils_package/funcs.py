from google.cloud import storage
import io
from PIL import Image

def list_objects(bucket_name, folder_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)
    return [blob.name for blob in blobs if blob.name.endswith((".jpg", ".png", ".jpeg"))]

def open_image_from_gcs(bucket_name, object_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    image_bytes = blob.download_as_bytes()
    image_file = io.BytesIO(image_bytes)
    image = Image.open(image_file)
    return image