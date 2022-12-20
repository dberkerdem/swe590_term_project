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
def write_image_to_s3(conn: object, fileobj: object, bucket: str, key: str) -> None:
    """
    Implementation of uploading images to s3 bucket
    :param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    :param fileobj: A file-like object to upload. At a minimum, it must implement the read method, and must return bytes
    :param bucket: The name of the bucket to upload to
    :param key: The name of the key to upload to
    :return: None, void function
    """
    # Upload file objects
    conn.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=key)
    # Close to connection to prevent bottleneck
    conn.close()


@boto3_connect(connect_to='sns')
def publish_sns(conn: object, message: str, ) -> None:
    """
    Implementation of publishing a message to SNS Topic
    :param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    :param message: Message to be published in SNS Topic
    :return: None, void function
    """
    # Publish a message
    conn.publish(
        TopicArn='arn:aws:sns:eu-west-1:624154963433:upload_complete_message',
        Message=message,
    )
    # Close to connection to prevent bottleneck
    conn.close()


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
