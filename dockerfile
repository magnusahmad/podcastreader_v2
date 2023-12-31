# Use an Ubuntu base image
FROM ubuntu:latest

# Update software repositories
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y pandoc python3 python3-pip python3-venv

# Install FFmpeg
RUN apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# (Optional) Add any other dependencies or perform configuration

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# (Optional) Expose ports, if your application requires it
EXPOSE 8080

# Create a Python virtual environment and activate it
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Command to run your application
CMD ["python3", "app.py"]
# Replace 'python' and 'app.py' with the command to run your application