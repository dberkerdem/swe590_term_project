import streamlit as st

uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

st.write("resulsts")