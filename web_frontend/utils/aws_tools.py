"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3

# Specify the bucket name
BUCKET_NAME = "swe590-bucket"
AWS_REGION = "eu-west-1"


def temporary_aws_handler(file):
    # client = boto3.client("s3", region_name=AWS_REGION)

    s3 = boto3.resource(
        service_name='s3',
        region_name=AWS_REGION,
    )

    s3.Bucket(BUCKET_NAME).put_object(Key='inputs/' + file.name, Body=file.type)
