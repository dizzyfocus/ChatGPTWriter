# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py .
COPY apikey.py .

# Expose the port that the application will run on (if applicable)
# EXPOSE <port_number>

# Set the environment variable
ENV OPENAI_API_KEY=<API KEY HERE>

# Run the Python application
CMD ["streamlit", "run", "--server.port", "8501", "app.py"]

