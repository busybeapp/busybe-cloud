# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8080

# Run the application with uvicorn
CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "8080"]
