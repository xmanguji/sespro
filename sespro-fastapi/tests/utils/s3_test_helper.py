from core.config import settings
from utils.s3_helper import client, delete_image


def clean_test_folder():
    """Help clean up S3 folder after Test
    """
    response = client.list_objects_v2(Bucket=settings.AWS_S3_BUCKET,
                                      Prefix=settings.AWS_S3_IMAGE_FOLDER)
    num = len(settings.AWS_S3_IMAGE_FOLDER)
    keys_list = response["Contents"]
    _list = []
    for keys in keys_list:
        _list.append(keys["Key"])

    for key in _list:
        key = (key[num:])
        delete_image(full_name=key)