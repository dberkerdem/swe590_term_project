"""Main method for lambda function in AWS"""
from src.utils.aws_tools import list_objects_in_s3, delete_object, read_object_from_s3, publish_sns
from src.preprocessing import preprocess
import time

BUCKET_NAME = 'swe590-bucket'
CSV_KEY = '/outputs/pixels.csv'
PREFIX = '/inputs/'


def lambda_handler(event, context):
    user_id = event.get('Records')[0].get('Sns').get('Message')
    print("User_id is:", user_id)
    prefix = user_id + PREFIX
    # Get List of objects in s3 bucket
    obj_list = list_objects_in_s3(bucket=BUCKET_NAME, prefix=prefix)
    # Print the items' keys
    pixels_list = list()
    try:
        for item in obj_list:
            print('Key is:', item.get('Key'))
            key = item.get('Key')
            # Load Image
            img_bytes = read_object_from_s3(bucket=BUCKET_NAME, key=key)
            # Preprocess Image
            pixels = preprocess.preprocess_images(img_bytes=img_bytes)
            pixels_list.append(pixels[0])
            # Delete the Image after preprocessed
            delete_object(bucket=BUCKET_NAME, key=key)
        print("Preprocessing completed")
        print("Bucket is unloaded")
    except TypeError as e:
        print(f"Bucket is empty. Exception: {e}")
    # Export CSV file
    csv_key = user_id + CSV_KEY
    preprocess.export_as_csv(pixels=pixels_list, bucket=BUCKET_NAME, key=csv_key)
    time.sleep(5)
    message = user_id
    # Publish message
    publish_sns(message=message)
    pass
