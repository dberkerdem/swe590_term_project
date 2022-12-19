"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3


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
            conn = boto3.client(connect_to)
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
    conn.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=key)
    # Close to connection to prevent bottleneck
    conn.close()


@boto3_connect(connect_to='sns')
def publish_sns(conn: object, message: str, ) -> None:
    """
    Implementation of publishing a message to a SNS Topic
    :param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    :param message: Message to be published in SNS Topic
    :return: None, void function
    """
    conn.publish(
        TopicArn='arn:aws:sns:eu-west-1:624154963433:upload_complete_message',
        Message=message,
    )
    # Close to connection to prevent bottleneck
    conn.close()
