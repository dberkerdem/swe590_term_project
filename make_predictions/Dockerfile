FROM public.ecr.aws/lambda/python:3.8
# Install the function's dependencies using file requirements.txt from your project folder.
COPY requirements.txt .

RUN pip3 install -r requirements.txt
# Copy files to your working directory
COPY . .

CMD ["lambda_function.lambda_handler"]
