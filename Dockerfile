# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Flyway 9.0.0
RUN apt-get update && apt-get install -y wget && \
    wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.0.0/flyway-commandline-9.0.0-linux-x64.tar.gz | tar xvz && \
    mv flyway-9.0.0 /usr/local/flyway && \
    ln -s /usr/local/flyway/flyway /usr/local/bin/flyway

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
# # ENV NAME World
ENV PYTHONPATH /app
# Run app.py when the container launches

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
