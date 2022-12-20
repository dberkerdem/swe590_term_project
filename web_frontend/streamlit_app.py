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

    # Initialize session state
    "st.session_state object:", st.session_state
    if 'index' not in st.session_state:
        st.session_state['index'] = 0

    # Initialize user_id to None
    user_id = None

    image_files = st.file_uploader("Upload an Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    for file in image_files:
        file.seek(0)

    submit = st.button("Submit Images")

    if image_files:
        if submit:
            user_id = str(uuid.uuid1())
            # Upload images to s3
            counter = 0
            for file in image_files:
                counter += 1
                write_image_to_s3(fileobj=file, bucket=BUCKET_NAME, key=user_id + DIR_NAME + file.name)
                print('upload Successful')
            st.success(f"{counter} Images Saved successfully!")
            # Wait 5 seconds after files are uploaded to s3 bucket
            time.sleep(5)
            message = user_id
            # Publish message
            publish_sns(message=message)

    if user_id:
        # Check s3 bucket for results
        print(f"user_id: {user_id}")
        is_exist = False
        while not is_exist:
            time.sleep(5)
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
    col1, col2, col3 = st.columns(1, 3, 1)

    # Display the uploaded images in a slideshow
    if image_files:
        # # Set the initial index to 0
        # index = 0

        # Add a "Next" button
        if st.session_state.index < len(image_files):
            if col3.button("Next"):
                st.session_state.index += 1
        if st.session_state.index > len(image_files):
            if col1.button("Back"):
                st.session_state.index += 1

        # Check if the index is still within the range of uploaded images
        if len(image_files) > st.session_state.index >= 0:
            col2.image(image_files[st.session_state.index], width=200)


if __name__ == '__main__':
    main()
