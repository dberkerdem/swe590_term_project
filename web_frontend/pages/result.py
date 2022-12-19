import streamlit as st
import boto3
import pandas as pd

st.cache

s3_client= boto3.client('s3')

st.title("Result Page")

folderName = st.text_input('Enter your folder name: ')

results = s3_client.get_object(Bucket='swe590_bucket', Key='output.csv')
dataset=pd.read_csv(results)
data=dataset['folderName']==folderName
print(data)


        