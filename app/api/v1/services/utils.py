"""
Services utils functions.
"""

from storage.service import upload_file
from logger.main import error_logger


###########################################
##            Common Utilities           ##
###########################################

async def update_image(image: str) -> str:
    """
    Update the url for image if it is new.
    """
    prefix = image.split(":")[0]
    if prefix == "data":
        try:
            new_image_url = await upload_file(file_base64=image)
        except Exception as ex:
            error_logger.register(ex)
            return image
        return new_image_url
    if prefix in ("https", "http", ""):
        return image
    return image
