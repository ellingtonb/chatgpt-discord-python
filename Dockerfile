FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

# Start the app
CMD [ "python", "./main.py" ]