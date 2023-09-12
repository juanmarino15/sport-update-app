FROM python:3.9
RUN apt-get update && apt-get install -y libpq-dev gcc


# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt from the project root into the container at /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the DataCollector contents to /app/ and the database folder to /app/database
COPY DataCollector/ .
COPY database/ database/

CMD ["python", "apiCollector.py"]
