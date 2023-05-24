# Using the base image
FROM python:3.11.3-alpine

# Installing dependencies
COPY . /app

# Устанавливаем зависимости
RUN pip3 install -r /app/requirements.txt

# Determine the working directory
WORKDIR /app

# Creating volume to save container data
VOLUME /app/data

# Launching the application
CMD ["python3", "main.py"]