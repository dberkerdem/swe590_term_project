import streamlit as st
import requests
import boto3
from PIL import Image

def load_image(image_file):
    img=Image.open(image_file)
    return img

AWS_REGION = "eu-west-1"

client = boto3.client("s3", region_name=AWS_REGION)

s3= boto3.resource (
    service_name='s3',
    region_name= AWS_REGION,
    aws_access_key_id='AKIAZCUUI5XU22BW27PF',
    aws_secret_access_key='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'
)


st.set_page_config(
    page_title="Multipage App"
)

st.title("Image Upload Page")
st.sidebar.success("Select a page above")


image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'], accept_multiple_files=True)
for file in image_file:
    file.seek(0)

if image_file is not None:
    for file in image_file:
        # display the name and the type of the file
        file_details = {"filename":file.name,
                        "filetype":file.type
        }
        st.write(file_details)

submit=st.button("Submit")

if image_file is not None:
    if submit:
        for file in image_file:
            s3.Bucket('swe590-bucket').put_object(Key=file.name,Body=file.type)
            message='File Uploaded Successfully'
            print('upload Successful')
            st.success("Saved successfully!")