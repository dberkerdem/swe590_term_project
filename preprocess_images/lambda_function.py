"""Main method for lambda function in AWS"""
from src.utils.aws_tools import list_objects_in_s3, empty_bucket, read_object_from_s3
from src.preprocessing import preprocess

BUCKET_NAME = 'swe590-bucket'
CSV_KEY = 'outputs/pixels.csv'


def lambda_handler(event, context):
    # Get List of objects in s3 bucket
    obj_list = list_objects_in_s3(bucket=BUCKET_NAME)
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
    except TypeError as e:
        print(f"Bucket is empty. Exception: {e}")
    # Empty the bucket
    empty_bucket(bucket=BUCKET_NAME)
    print("Bucket is unloaded")
    # Export CSV file
    preprocess.export_as_csv(pixels=pixels_list, bucket=BUCKET_NAME, key=CSV_KEY)
    pass
