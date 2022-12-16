import streamlit as st
import requests


st.title("Result Page")

results=requests.get('https://myservice.com/multiply_by_2')

st.write(results)