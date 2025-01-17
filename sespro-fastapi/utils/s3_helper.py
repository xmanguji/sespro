from datetime import datetime

from typing import Any, Dict, Union
import boto3
import logging
from uuid import uuid4

from botocore.config import Config
from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from pydantic.types import Json

from core.config import settings

logger = logging.getLogger(__name__)

client = boto3.client(
    "s3", config=Config(signature_version="s3v4"), region_name=settings.AWS_REGION
)

BUCKET_NAME = "blogsource"


def generate_random_name() -> str:
    name = str(uuid4())
    return name


def generate_name_by_time(location: str) -> str:
    timestamp = str(datetime.utcnow())
    timestamp_list = timestamp.split()
    name = location + "_" + timestamp_list[0] + "_" + timestamp_list[1]
    return name


def delete_image(
    full_name, bucket_name: str = settings.AWS_S3_BUCKET
) -> Union[Dict[str, Any], bool]:
    """Delete an Image

    Args:
        full_name (str): The image full key
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.

    Returns:
        Union[Dict[str, Any], bool]: The Response
    """
    try:
        response = client.delete_object(Bucket=bucket_name, Key=f"image/{full_name}")
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    if response["ResponseMetadata"]["HTTPStatusCode"] > 399:
        return {"success": False}

    return {"success": True}


def get_image(
    full_name, bucket_name: str = settings.AWS_S3_BUCKET
) -> Dict[str, Union[str, bool]]:
    """Get Image

    Args:
        full_name ([type]): The image full key
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.

    Returns:
        Dict[str, Union[str, bool]]: The response
    """

    try:
        response = client.get_object(Bucket=bucket_name, Key=full_name)
    except ClientError as e:
        logger.error(e)
        return {"success": False}
    return {"success": True, "image_byte": response["Body"]}


def store_image(
    image: bytes,
    bucket_name: str = settings.AWS_S3_BUCKET,
    ext: str = ".jpeg",
    uuid: str = str(uuid4())
) -> Dict[str, Union[str, bool]]:
    """Store Images

    Args:
        image (bytes): The image object
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.
        ext (str, optional): the file extension. Defaults to ".jpeg".
        uuid (str): parsed audit uuid + parsed question uuid separated by '_'
    Returns:
        Dict[str, Union[str, bool]]: The Response
    """

    key = settings.AWS_S3_IMAGE_FOLDER + uuid + ext

    try:
        response = client.put_object(
            Bucket=bucket_name, Body=image, Key=key, ACL="public-read"
        )
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    return {"success": True, "image_key": key, "uri": url}


def get_raw_data(
    key: str, bucket_name: str = settings.AWS_S3_BUCKET
) -> Dict[str, Union[StreamingBody, bool]]:
    """Get Raw Data

    Args:
        key (str): The object key
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.

    Returns:
        Dict[str, Union[str, bool]]: The response
    """

    try:
        response = client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    return {"success": True, "obj_json": response["Body"]}


def store_raw_data(
    location: str,
    _object: Json,
    bucket_name: str = settings.AWS_S3_BUCKET,
    ext: str = ".json",
    uuid: str = str(uuid4()),
) -> Dict[str, Union[str, bool]]:
    """Store Raw Data (Json)

    Args:
        location (str): the premises for which data was generated
        _object (Json): The json object to store
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.
        ext (str, optional): the file extension. Defaults to ".json".
        uuid (str): the parsed audit uuid

    Returns:
        Dict[str, Union[str, bool]]: The Response
    """

    key = settings.AWS_S3_DATA_FOLDER + uuid + ext

    try:
        response = client.put_object(Bucket=bucket_name, Body=_object, Key=key)
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    uri = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    return {"success": True, "obj_key": key, "uri": uri}


def delete_raw_data(
    full_name, bucket_name: str = settings.AWS_S3_BUCKET
) -> Union[Dict[str, Any], bool]:
    """Delete stored Raw Data

    Args:
        full_name (str): The raw_data full key
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.

    Returns:
        Union[Dict[str, Any], bool]: The Response
    """
    try:
        response = client.delete_object(
            Bucket=bucket_name, Key=f"{settings.AWS_S3_DATA_FOLDER}/{full_name}"
        )
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    if response["ResponseMetadata"]["HTTPStatusCode"] > 399:
        return {"success": False}

    return {"success": True}


def store_remapped_data(
    location: str,
    _object: Json,
    bucket_name: str = settings.AWS_S3_BUCKET,
    ext: str = ".json",
) -> Dict[str, Union[str, bool]]:
    """Store Raw Data (Json)

    Args:
        location (str): the premises for which data was generated
        _object (Json): The json object to store
        bucket_name (str, optional): The bucket name. Defaults to settings.AWS_S3_BUCKET.
        ext (str, optional): the file extension. Defaults to ".json".

    Returns:
        Dict[str, Union[str, bool]]: The Response
    """

    name = generate_name_by_time(location)
    key = settings.AWS_S3_REMAP_FOLDER + name + ext

    try:
        response = client.put_object(Bucket=bucket_name, Body=_object, Key=key)
    except ClientError as e:
        logger.error(e)
        return {"success": False}

    uri = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    return {"success": True, "obj_key": key, "uri": uri}
