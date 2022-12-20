import streamlit as st
from utils.aws_tools import write_image_to_s3, publish_sns, read_object_from_s3
import time
import uuid

BUCKET_NAME = "swe590-bucket"
DIR_NAME = "/inputs/"
RESULTS_KEY = '/results/results.csv'


def main():
    st.set_page_config(
        page_title="SWE-590",
        layout="wide"
    )
    st.title("Upload.py your Images")
    # st.sidebar.success("Select a page")

    # Initialize user_id to None
    user_id = None

    image_file = st.file_uploader("Upload.py An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    for file in image_file:
        file.seek(0)

    submit = st.button("Submit Images")

    uploaded_files = list()
    if image_file is not None:
        if submit:
            user_id = str(uuid.uuid1())
            # Upload images to s3
            counter = 0
            for file in image_file:
                counter += 1
                write_image_to_s3(fileobj=file, bucket=BUCKET_NAME, key=user_id + DIR_NAME + file.name)
                print('upload Successful')
                uploaded_files.append(file.name)
            st.success(f"{counter} Images Saved successfully!")
            # Wait 5 seconds after files are uploaded to s3 bucket
            time.sleep(5)
            message = user_id
            # Publish message
            publish_sns(message=message)

    if user_id:
        ###########################################
        # TODO - Afize: Insert slideshow here
        ###########################################
        print(f"user_id: {user_id}")
        time.sleep(5)
        is_exist = False
        while not is_exist:
            time.sleep(3)
            try:
                # get object
                results_key = user_id + RESULTS_KEY
                file_obj = read_object_from_s3(bucket=BUCKET_NAME, key=results_key)
                # Get lines of csv
                lines = file_obj.get('Body').read().decode('utf-8').splitlines()
                # Set the results
                results = ' '.join(lines[1:])
                # Write the results
                st.write(results)
                # set flag true
                is_exist = True
                print(f"Results: {results}")
            except Exception as e:
                print(f"Exception {e}")
        pass


if __name__ == '__main__':
    main()
