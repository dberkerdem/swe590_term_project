"""aws_tools script contains utility functions to perform read and write operations to AWS"""
import boto3
import pickle
from src.utils.config import load_config


# Specify the bucket name
bucket_name = "swe590-bucket"


def boto3_connect(connect_to: str, func: function):
    """
    Implementation of boto3 client wrapper.
    Creates a boto3 connection client object to the AWS resource of interest, and pass the object to wrapped function.
    @param connect_to: a str, that corresponds to the resource name to the connection client to be established
    @param func: a function to be wrapped
    @return: a wrapped function, that wraps the input function 
    """
    def wrapper(*args, **kwargs):
        conn = boto3.client("s3")
        return func(conn=conn, *args, **kwargs)
    return wrapper


def generate_aws_key(params: dict, dtype: str, mode: str = None, file_name: str = "aws.yml") -> str:
    """
    Implementation of aws key generating method.
    Generates a s3 key, that point towards to the location of the object at s3
    @param params: a dictionary, that contains required parameters in request
    @param dtype: a string, that represents dtype of the media to be read or written
    @param mode: a string, that represent mode of operation
    @param file_name: a string, name of the config file that contains variables for AWS
    @return: a string, that points towards to the location of the object at s3
    """
    aws_config = load_config(file_name=file_name).get('s3').get(f'{dtype}')
    name = aws_config.get("name")
    # Generate AWS Key
    if dtype == "model":
        key = f'{params.get("x-api-key")}/{params.get("asset-id")}/' \
              f'{dtype}/method-{params.get("modelling-method")}/{name}'
    elif dtype == "media":
        if mode == "read":
            mode_fix = f"input/{params.get('pipeline')}"
        elif mode == "write":
            mode_fix = f"output/method-{params.get('modelling-method')}"
        key = f"{params.get('x-api-key')}/{params.get('asset-id')}/{mode_fix}/{name}"
    return key


@boto3_connect(connect_to='s3')
def write_model_to_s3(conn: object, model: dict, params: dict) -> str:
    """
    Implementation of saving a trained model to S3 bucket. Generates the s3 key by calling generate_aws_key function
    and puts the object to the location that the key directs
    @param conn: an object, that is a connection client to the AWS resource of interest, in this case s3
    @param model: a dictionary, trained model that contains analytic parameters
    @param params: a dictionary, that contains required parameters in request
    @return: a string, Success messages if saved else raises an exception
    """
    # Generate the key
    key = generate_aws_key(params=params, dtype="model", )
    try:
        serialized_model = pickle.dumps(model)
        conn.put_object(Bucket=bucket_name, Key=key, Body=serialized_model)
        return "Model is successfully saved to s3"
    except Exception as e:
        raise Exception(f"An error occurred during saving model to s3. Error: {e}")


@boto3_connect(connect_to='s3')
def read_model_from_s3(conn: object, params: dict):
    """
    Implementation of loading a trained model from s3 bucket. Generates the s3 key by calling generate_aws_key function
    and loads the object from the location that the key directs
    @param conn: an object, that is a connection client to the AWS resource of interest, in this case s3
    @param params: a dictionary, that contains required parameters in request
    @return: a dictionary, returns a trained model that contains analytic parameters
    """
    # Generate the key
    key = generate_aws_key(params=params, dtype="model", )
    try:
        model_from_s3 = pickle.loads(conn.Bucket(bucket_name).Object(key).get()['Body'].read())
        return model_from_s3
    except Exception as e:
        raise Exception(f"An error occurred during loading model from s3. Error: {e}")


@boto3_connect(connect_to='s3')
def read_data_from_s3(conn: object, params: dict):
    """
    Implementation of loading data from s3 bucket. Generates the s3 key by calling generate_aws_key function
    and loads the object from the location that the key directs
    @param conn: an object, that is a connection client to the AWS resource of interest, in this case s3
    @param params: a dictionary, that contains required parameters in request
    @return: a dictionary, that contains mechanical current data
    """
    # Generate the key
    key = generate_aws_key(params=params, dtype="media", mode="read")
    try:
        response = conn.get_object(Bucket=bucket_name, Key=key)
        data = response["Body"].read().decode()
        return data
    except Exception as e:
        raise Exception(f'Error getting object from key: {key}, from bucket: {bucket_name}. '
                        f' Make sure that you have uploaded a file to the signed URL. '
                        f'Error: {e}')


@boto3_connect(connect_to='s3')
def write_data_to_s3(conn: object, data: list, params: dict) -> dict:
    """
    Implementation of saving anomaly score data to S3 bucket. Generates the s3 key by calling generate_aws_key function
    and puts the object to the location that the key directs
    @param conn: an object, that is a connection client to the AWS resource of interest, in this case s3
    @param data: a list, that contains anomaly score data generated in predict pipeline
    @param params: a dictionary, that contains required parameters in request
    @return: a dictionary, that contains the pre-signed URL where the customer can access the anomaly score data
    for a limited amount of time
    """
    # Generate the key
    key = generate_aws_key(params=params, dtype="media", mode="write")
    try:
        serialized_data = pickle.dumps(data)
        conn.put_object(Bucket=bucket_name, Key=key, Body=serialized_data)
        return get_pre_signed_url(key=key, client=conn)
    except Exception as e:
        raise Exception(f'Error putting object with key: {key}, to bucket: {bucket_name}. '
                        f'Make sure that you have uploaded a file to the signed URL. '
                        f'Error: {e}')


def get_pre_signed_url(key: str, client: object) -> dict:
    """
    Implementation of getting pre-signed URL from s3 bucket, which is located by key
    @param key: a string, that points towards to the location of the object at s3
    @param s3: an object, connector object to the s3 bucket
    @return: a string, that points towards to the location of the object at s3
    """
    # Get the pre-signed url
    pre_signed_url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key
        },
        ExpiresIn=3000  # Expires in 5 minutes
    )
    return pre_signed_url
