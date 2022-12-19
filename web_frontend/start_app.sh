sh -c 'docker build -t web_frontend . &&
docker run -it -p 8501:8501 web_frontend'