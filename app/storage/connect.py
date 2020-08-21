"""
Google Cloud Storage connection.
"""

from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError
from config import settings  # pylint: disable-msg=E0611


async def get_storage_bucket():
    """
    Return a GCP bucket-storage client.
    """
    buckent_name = settings.GOOGLE_STORAGE_BUCKET
    try:
        client = storage.Client()
    except DefaultCredentialsError:
        client = storage.Client(settings.GOOGLE_APPLICATION_CREDENTIALS)
    except Exception:
        return False
    bucket = client.bucket(buckent_name)
    return bucket
