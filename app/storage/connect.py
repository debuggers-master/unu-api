"""
Google Cloud Storage - Connection.
"""

from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

from logger.main import error_logger
from config import settings  # pylint: disable-msg=E0611


###########################################
##           Bucket Connection           ##
###########################################

async def get_storage_bucket():
    """
    Return a GCP bucket-storage client.
    """
    buckent_name = settings.GOOGLE_STORAGE_BUCKET
    try:
        client = storage.Client()
    # except DefaultCredentialsError:
    #     client = storage.Client(settings.GOOGLE_APPLICATION_CREDENTIALS)
    except Exception as ex:  # pylint: disable-msg=W0703
        await error_logger.register(ex)
        return False
    bucket = client.bucket(buckent_name)
    return bucket
