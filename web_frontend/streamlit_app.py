import streamlit as st
from utils.aws_tools import write_image_to_s3
# from streamlit_toggle import st_toggle_switch
import time

BUCKET_NAME = "swe590-bucket"
DIR_NAME = "inputs/"


def main():
    st.set_page_config(
        page_title="SWE-590",
        layout="wide"
    )

    st.title("Upload.py your Images")
    st.sidebar.success("Select a page")

    image_file = st.file_uploader("Upload.py An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    for file in image_file:
        file.seek(0)

    submit = st.button("Submit Images")
    show_details = st.button("Show Upload.py Details")

    if image_file is not None:
        if show_details:
            for file in image_file:
                # display the name and the type of the file
                file_details = {"filename": file.name,
                                "filetype": file.type
                                }
                st.write(file_details)

    if image_file is not None:
        if submit:
            for file in image_file:
                write_image_to_s3(fileobj=file, bucket=BUCKET_NAME, key=DIR_NAME + file.name)
                print('upload Successful')
                st.success("Saved successfully!")
        # Wait 10 seconds after files are uploaded to s3 bucket
        time.sleep(10)



if __name__ == '__main__':
    main()
