"""
Storage files functions.
"""

from uuid import uuid4
from datetime import datetime
import os
import base64

from fastapi import status, HTTPException, UploadFile
import six

from config import settings  # pylint: disable-msg=E0611
from .connect import get_storage_bucket


def _check_extension(filename: str) -> None:
    """
    Check if the extension is allowed.
    """
    _, ext = os.path.splitext(filename)
    if ext.replace(".", "") not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The image extension can only be {settings.ALLOWED_EXTENSIONS}"
        )


def _unique_filename(filename: str) -> str:
    """
    Generates a unique filename that is unlikely to collide with existing
    objects in Google Cloud Storage.
    """
    date = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}-{2}.{3}".format(basename, date, str(uuid4()), extension)


async def upload_file(file_base64: str = "", file: UploadFile = None) -> str:
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.

    Params:
    ------
    file_base64: str - The file to upload encoded in base 64.
    file: UploadFile - The file to upload
    * You only pass one option.

    Return:
    ------
    url: str - The file public url
        If some error occurs. Return False.
    """

    if file_base64:
        metadata: list = file_base64.split(";")
        content_type: str = metadata[0][5:]
        file_data: bytes = base64.b64decode(metadata[1][7:])
        ext: str = content_type.split("/")[1]
        filename = f"avatar-unu.{ext}"
    else:
        filename = file.filename
        content_type = file.content_type
        file_stream = file.file

    _check_extension(filename)

    filename = _unique_filename(filename)
    bucket = await get_storage_bucket()

    try:
        blob = bucket.blob(filename)
    except (AttributeError, KeyError):
        # If the bucket is missing cause credential exception
        return False

    if file_base64:
        blob.upload_from_string(file_data, content_type=content_type)
    else:
        blob.upload_from_file(file_stream, content_type=content_type)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')
    return url
