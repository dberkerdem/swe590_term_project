import streamlit as st
import requests

st.set_page_config(
    page_title="Multipage App"
)

st.title("Image Upload Page")
st.sidebar.success("Select a page above")

uploaded_images = st.file_uploader("Choose images", accept_multiple_files=True)

submit=st.button("Submit")

if submit:
    resp = requests.post('https://myservice.com/multiply_by_2', data={'uploadedimages': uploaded_images})
    st.write("Your request is saved. Go to the result page to see results.")