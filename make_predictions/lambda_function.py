"""Main method for lambda function in AWS"""
from src.utils.aws_tools import read_object_from_s3, delete_object
from src.modelling import predict

BUCKET_NAME = 'swe590-bucket'
CSV_KEY = '/outputs/pixels.csv'
MODEL_KEY = './cnn_model.h5'
RESULTS_KEY = '/results/results.csv'


def lambda_handler(event, context):
    # Get user_id
    user_id = event.get('Records')[0].get('Sns').get('Message')
    # Create csv_key
    csv_key = user_id + CSV_KEY
    # Get Object
    file_obj = read_object_from_s3(bucket=BUCKET_NAME, key=csv_key)
    # Delete object from s3
    delete_object(bucket=BUCKET_NAME, key=csv_key)
    # Prepare Object
    pixels_data = predict.prepare_data(file_obj=file_obj)
    # Make Predictions
    predictions = predict.cnn_predict(data=pixels_data, key=MODEL_KEY)
    # Export Results as CSV
    results_key = user_id + RESULTS_KEY
    predict.export_as_csv(data=predictions, bucket=BUCKET_NAME, key=results_key)


if __name__ == '__main__':
    lambda_handler()
