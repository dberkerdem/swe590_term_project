"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3


def boto3_connect(connect_to: str):
    """
    Implementation of boto3 client wrapper.
    Creates a boto3 connection client object to the AWS resource of interest, and pass the object to wrapped function.
    @param connect_to: a str, that corresponds to the resource name to the connection client to be established
    @return: a decorator
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = boto3.client(connect_to)
            return func(conn=conn, *args, **kwargs)

        return wrapper

    return decorator


@boto3_connect(connect_to='s3')
def list_objects_in_s3(conn: object, bucket: str) -> list:
    """
    Implementation of listing all key of all objects within a bucket
    @param conn: A low-level client representing Amazon Resources
    @param bucket: The name of the bucket containing the objects
    @return:
    """
    obj_list = conn.list_objects(
        Bucket=bucket,
    )
    # Return the list of contents
    return obj_list.get('Contents')


@boto3_connect(connect_to='s3')
def read_object_from_s3(conn: object, bucket: str, key: str):
    """
    Implementation of reading objects from s3 bucket
    @param conn: A low-level client representing Amazon Resources
    @param bucket: The name of the bucket to upload to
    @param key: The name of the key to upload to
    @return: None, void function
    """
    # Get the object from bucket
    obj = conn.get_object(Bucket=bucket, Key=key)
    data = obj["Body"].read()
    # Close to connection to prevent bottleneck
    conn.close()
    return data


def empty_bucket(bucket: str):
    """
    Implementation of deleting all objects withing s3 bucket
    @param bucket: Bucket to be discharged
    @return: None, void function
    """
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket)
    bucket_versioning = s3.BucketVersioning(bucket)
    if bucket_versioning.status == 'Enabled':
        s3_bucket.object_versions.delete()
    else:
        s3_bucket.objects.all().delete()
    print("Bucket is cleaned.")


@boto3_connect(connect_to='s3')
def write_object_to_s3(conn: object, bucket: str, body: object, key: str) -> None:
    """
    Implementation of uploading object to s3 bucket
    @param body:
    @param conn: a boto3 client object, that establishes a connection to the AWS resource of interest
    @param bucket: The name of the bucket to upload to
    @param key: The name of the key to upload to
    @return: None, void function
    """
    # Upload file objects
    conn.put_object(Bucket=bucket, Body=body, Key=key)
    # Close to connection to prevent bottleneck
    conn.close()
