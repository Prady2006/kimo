FROM nikolaik/python-nodejs:python3.11-nodejs18-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
