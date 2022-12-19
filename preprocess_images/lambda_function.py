"""Main method for lambda function in AWS"""
from src.utils.aws_tools import list_objects_in_s3, empty_bucket, read_image_from_s3
from PIL import Image
import numpy as np
import io

BUCKET_NAME = 'swe590-bucket'


def lambda_handler(event, context):
    # Get List of objects in s3 bucket
    obj_list = list_objects_in_s3(bucket=BUCKET_NAME)
    # Print the items' keys
    pixels_list = list()
    try:
        for item in obj_list:
            print(item.get('Key'))
            key = item.get('Key')
            # Load Image
            img = read_image_from_s3(bucket=BUCKET_NAME, key=key)
            # # Preprocess Image
            # reshaped_array = preprocess_images(...)
            # pixels_list.append(reshaped_array[0])
        img_bytes = read_image_from_s3(bucket=BUCKET_NAME, key=key)
        img = np.array(Image.open(io.BytesIO(img_bytes)))
        greyscale_img = Image.fromarray(img).convert('L')
        print(type(img))
        print(type(greyscale_img))
        print(img)
    except TypeError as e:
        print(f"Bucket is empty. Exception: {e}")
    # Empty the bucket
    # empty_bucket(bucket=BUCKET_NAME)
    return 0

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
