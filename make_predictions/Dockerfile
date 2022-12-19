#FROM tensorflow/tensorflow:latest
#
## Set the working directory to /app
#WORKDIR /app
## Copy function code
#COPY requirements.txt /app
## Install the function's dependencies using file requirements.txt from your project folder.
#RUN  pip3 install --upgrade pip
#
## Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt
#
## Copy files to your working directory
#COPY . /app
## Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
#CMD ["lambda_function.lambda_handler"]

FROM public.ecr.aws/lambda/python:3.7

RUN pip3 install --upgrade pip3
RUN pip3 install -r requirements.txt
RUN pip3 install https://bit.ly/tflite-centos-py37-whl
COPY . .
CMD ["lambda_function.lambda_handler"]