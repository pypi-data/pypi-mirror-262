import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)
# disable boto logs
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)

s3_client = boto3.client("s3", config=Config(max_pool_connections=20))


def upload_file_to_s3(bucket_name, local_path, s3_path, s3_url, relative_path):
    s3_client.upload_file(local_path, bucket_name, s3_path)
    logger.debug(f"Uploaded {local_path} to {s3_url}/{relative_path}")


def write_flag_to_s3(state, s3_url):
    bucket_name, s3_prefix = _parse_s3_url(s3_url)

    # delete all other files starting with "flag."
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
        if "Contents" in response:
            for obj in response["Contents"]:
                if obj["Key"].startswith(f"{s3_prefix}/flag."):
                    s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
    except KeyError:
        pass

    time_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    s3_path = os.path.join(s3_prefix, f"flag.{state}").replace("\\", "/")
    s3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=time_now)
    logger.debug(f"Created flag file for {state} state at s3://{bucket_name}/{s3_path}")


def upload_to_s3(s3_url, directory_path):
    bucket_name, s3_prefix = _parse_s3_url(s3_url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(
                upload_file_to_s3,
                bucket_name,
                os.path.join(root, file),
                os.path.join(
                    s3_prefix, os.path.relpath(os.path.join(root, file), directory_path)
                ).replace("\\", "/"),
                s3_url,
                os.path.relpath(os.path.join(root, file), directory_path),
            )
            for root, _, files in os.walk(directory_path)
            for file in files
            if not file.startswith("flag.")  # Skip flag files
        ]
        # Wait for all upload tasks to complete
        for future in futures:
            future.result()


def download_file_from_s3(s3_url, destination_path):
    bucket_name, s3_prefix = _parse_s3_url(s3_url)

    s3_client.download_file(bucket_name, s3_prefix, destination_path)


def _parse_s3_url(s3_url):
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    s3_prefix = parsed_url.path.lstrip("/")  # Remove leading '/' from path
    return bucket_name, s3_prefix
