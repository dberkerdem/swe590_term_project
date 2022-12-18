"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3


def write_image_to_s3(fileobj: object, bucket: str, key: str) -> None:
    """
    """
    conn = boto3.client("s3")
    conn.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=key)
