from PIL import Image
import numpy as np
import io
import pandas as pd
from ..utils.aws_tools import write_object_to_s3


def preprocess_images(img_bytes: bytes) -> list:
    """
    Implementation of preprocessing of an image. Takes bytes array of an image with 28x28 resolution as input
    and converts it to pixels array of 1x784
    @param img_bytes: Bytes array of image
    @return: Pixels list with a length of 784
    """
    # Convert bytes array of RGB Image to numpy array
    img = np.array(Image.open(io.BytesIO(img_bytes)))
    # Convert to grayscale
    greyscale_img = Image.fromarray(img).convert('L')
    # Convert to numpy array of pixels
    greyscale_array = np.array(greyscale_img)
    # Reshape from (28,28) to (1,784) for csv
    reshaped_array = greyscale_array.reshape(1, 784)
    return reshaped_array


def export_as_csv(pixels: list, bucket: str, key: str) -> None:
    """
    Implementation of exporting a list
    @param pixels: Pixels list with a length of n rows and 784 columns
    @param bucket: The name of the bucket to upload to
    @param key: The name of the key to upload to
    @return:None, void
    """
    pixels_df = pd.DataFrame(pixels)
    # Add column name prefix
    pixels_df.columns = ['pixel_' + str(col) for col in pixels_df.columns]
    # Create a buffer
    csv_buffer = io.StringIO()
    # Fill the buffer
    pixels_df.to_csv(csv_buffer, header=True, index=False)
    csv_buffer.seek(0)
    # Write to s3 as csv
    write_object_to_s3(bucket=bucket, body=csv_buffer.getvalue(), key=key)
