# app/Dockerfile
# GUIDE FOR STREAMLIT DOCKERIZATION: https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
FROM python:3.8-slim

EXPOSE 8501

WORKDIR /web_frontend

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*  &&\
    python -m pip install --upgrade pip
COPY requirements.txt /web_frontend/

RUN pip3 install -r requirements.txt

COPY . /web_frontend/

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
