"""Main method for lambda function in AWS"""
from PIL import Image
import numpy as np
import pandas as pd


def lambda_handler(event, context):
    # Load .png from s3

    # Convert to the usable format
    pixels_list = list()
    for img in images:
        # Convert to grayscale
        greyscale_img = Image.fromarray(img).convert('L')
        # Convert to numpy array of pixels
        greyscale_array = np.array(greyscale_img)
        # Reshape from (28,28) to (1,784) for csv
        reshaped_array = greyscale_array.reshape(1, 784)
        # Append row to dataframe
        pixels_list.append(reshaped_array[0])
    # Convert to dataframe
    pixels_df = pd.DataFrame(pixels_list)
    # Add column name prefix
    pixels_df.columns = ['pixel' + str(col) for col in pixels_df.columns]
    # Write to s3 as csv
    pixels_df.to_csv("pixels_csv")
    pass
