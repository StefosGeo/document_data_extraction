# Use an official Python runtime as the base image
FROM python:3.9-slim
RUN pip install --upgrade pip==23.2.1

# Set the working directory in the container
WORKDIR /llm_data_parser

# Copy the local directory content (from your machine) to the container
COPY . /llm_data_parser/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container (optional, if you need a port)
# EXPOSE 80

# Set the default command to execute
# It might be your main script or another command you'd like to run when the container starts
CMD ["python", "main.py"]
