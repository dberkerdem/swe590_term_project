"""Main method for lambda function in AWS"""
from src.utils.aws_tools import read_object_from_s3, empty_bucket
from src.modelling import predict

BUCKET_NAME = 'swe590-bucket'
CSV_KEY = 'outputs/pixels.csv'
MODEL_KEY = 'cnn_model.h5'
RESULTS_KEY = 'results/results.csv'


def lambda_handler(event, context):
    # Get Object
    file_obj = read_object_from_s3(bucket=BUCKET_NAME, key=CSV_KEY)
    # Prepare Object
    pixels_data = predict.prepare_data(file_obj=file_obj)
    # Make Predictions
    predictions = predict.cnn_predict(data=pixels_data, key=MODEL_KEY)
    # Empty the Bucket
    empty_bucket(bucket=BUCKET_NAME)
    # Export Results as CSV
    predict.export_as_csv(input_list=predictions, bucket=BUCKET_NAME, key=RESULTS_KEY)


if __name__ == '__main__':
    lambda_handler()
