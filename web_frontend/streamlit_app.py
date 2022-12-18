import streamlit as st
from utils.aws_tools import temporary_aws_handler


def main():
    st.set_page_config(
        page_title="Multipage App"
    )

    st.title("Image Upload Page")
    st.sidebar.success("Select a page above")

    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    for file in image_file:
        file.seek(0)

    if image_file is not None:
        for file in image_file:
            # display the name and the type of the file
            file_details = {"filename": file.name,
                            "filetype": file.type
                            }
            st.write(file_details)

    submit = st.button("Submit")

    if image_file is not None:
        if submit:
            for file in image_file:
                temporary_aws_handler(file=file)
                print('upload Successful')
                st.success("Saved successfully!")


if __name__ == '__main__':
    main()
