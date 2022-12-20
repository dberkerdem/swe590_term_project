import tensorflow as tf
import pandas as pd
import io
import numpy as np
from ..utils.aws_tools import write_object_to_s3


def prepare_data(file_obj: object, image_res: int = 28) -> pd.DataFrame:
    # Get the body
    body = file_obj.get('Body')
    # Decode content
    csv_string = body.read().decode('utf-8')
    # Convert to DataFrame
    data = pd.read_csv(io.StringIO(csv_string))
    print("Shape of data is:", data.shape)
    # Multiply negative values with -1
    cols = data.select_dtypes(np.number).columns
    data[cols] = data[cols].abs()
    # Reshape the DataFrame
    data_reshaped = data.values.reshape(-1, image_res, image_res, 1) / 255.
    return data_reshaped


def cnn_predict(data: pd.DataFrame, key: str) -> pd.DataFrame:
    model = load_model(key=key)
    pred = model.predict(data)
    pred_ = np.argmax(pred, axis=1)
    return pred_


def load_model(key: str):
    loaded_model = tf.keras.models.load_model(key)
    return loaded_model


def export_as_csv(data, bucket: str, key: str) -> None:
    """
    Implementation of exporting a list
    @param data: Input data
    @param bucket: The name of the bucket to upload to
    @param key: The name of the key to upload to
    @return:None, void
    """
    if isinstance(data, list):
        outgoing_df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        outgoing_df = data
    elif isinstance(data, np.ndarray):
        outgoing_df = pd.DataFrame(data)
    else:
        raise Exception(f"Invalid input type: {type(data)}")
    # Create a buffer
    csv_buffer = io.StringIO()
    # Fill the buffer
    outgoing_df.to_csv(csv_buffer, header=True, index=False)
    csv_buffer.seek(0)
    # Write to s3 as csv
    write_object_to_s3(bucket=bucket, body=csv_buffer.getvalue(), key=key)
