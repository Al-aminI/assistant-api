# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr  libsm6 libxext6 poppler-utils  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install pytesseract
RUN pip install opencv-python
RUN pip install pillow
RUN python -m pip install psycopg2-binary
# RUN apt-get install libllvm12:i386
RUN  apt-get install libglib2.0-0

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
# Copy the requirements.txt file into the container and install Python packages
COPY requirements.txt /app/
RUN pip install  --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port (adjust the port number as needed)
EXPOSE 80


# Start your application
CMD ["python", "manage.py", "run"]
