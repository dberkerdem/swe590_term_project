FROM python:3.8-slim

# Copy function code
COPY requirements.txt .

# Install the function's dependencies using file requirements.txt
# from your project folder.
RUN  pip3 install --upgrade pip
RUN  pip3 install -r requirements.txt --target .
# Copy files to your working directory
COPY . .
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
