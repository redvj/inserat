# Use the official Python 3.10 image as the base image
FROM python:3.10-slim-buster

# Add user 'inserat' and set the working directory
RUN useradd inserat
WORKDIR /home/inserat

# Copy the requirements file and install dependencies
COPY ./requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install gunicorn pymysql cryptography

# Copy application files and adjust permissions
COPY app app
COPY migrations migrations
COPY app.py config.py boot.sh .env ./
COPY flask_uploads.py /home/inserat/venv/lib/python3.10/site-packages/
RUN chmod 755 /home/inserat/venv/lib/python3.10/site-packages/flask_uploads.py

# Set environment variable for Flask
ENV FLASK_APP app.py

# Set user permissions for the container
RUN chown -R inserat:inserat ./

# Expose port 5000 for the container
EXPOSE 5000

# Define the entry point for the application
ENTRYPOINT ["./boot.sh"]
