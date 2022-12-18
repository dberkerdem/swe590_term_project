import streamlit as st
import requests


st.title("Result Page")

results=requests.get('http://localhost:8888/tree/Untitled%20Folder%202')

st.write(results)