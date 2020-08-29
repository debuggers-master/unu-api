"""
Upload file testing
"""
import pytest
from app.storage.service import upload_file


# @pytest.mark.skip(reason="No uploan many files")
@pytest.mark.asyncio
async def test_upload_file_b64():
    """
    Upload file testing
    """
    with open("tests/storage/image.txt", "r") as f:
        image = f.readline()

    url = await upload_file(file_base64=image)
    assert url.split("-")[0] == "https://storage.googleapis.com/unu"
