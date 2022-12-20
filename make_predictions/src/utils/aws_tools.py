"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3

REGION_NAME = 'eu-west-1'


def boto3_connect(connect_to: str):
    """
    Implementation of boto3 client wrapper.
    Creates a boto3 connection client object to the AWS resource of interest, and pass the object to wrapped function.
    @param connect_to: a str, that corresponds to the resource name to the connection client to be established
    @param func: a function to be wrapped
    @return: a decorator
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = boto3.client(connect_to, region_name=REGION_NAME)
            return func(conn=conn, *args, **kwargs)

        return wrapper

    return decorator


@boto3_connect(connect_to='s3')
def read_object_from_s3(conn: object, bucket: str, key: str):
    """
    Implementation of reading an object from s3
    @param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    @param bucket: Name of the bucket
    @param key: Key of the object
    @return:
    """
    obj = conn.get_object(Bucket=bucket, Key=key)
    # conn.close()
    return obj


@boto3_connect(connect_to='s3')
def write_object_to_s3(conn: object, bucket: str, body: object, key: str) -> None:
    """
    Implementation of uploading object to s3 bucket
    @param body: Object to be put
    @param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    @param bucket: The name of the bucket to upload to
    @param key: The name of the key to upload to
    @return: None, void function
    """
    # Upload file objects
    conn.put_object(Bucket=bucket, Body=body, Key=key)
    pass


@boto3_connect(connect_to='s3')
def delete_object(conn: object, bucket: str, key: str) -> None:
    """
    Implementation of deleting an object from s3 bucket
    @param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    @param bucket: The name of the bucket
    @param key: Key to the object
    @return: None, void function
    """
    response = conn.delete_object(
        Bucket=bucket,
        Key=key,
    )
