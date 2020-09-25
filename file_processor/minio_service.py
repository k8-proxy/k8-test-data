import os
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:minio")


class Minio:
    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def download_files(self, bucket_name, file_name):

        try:
            self.s3.Bucket(bucket).download_file(file_name, file_name + "/" + file_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.info("The object does not exist.")
            else:
                logger.info(e)
                raise