FROM python:3.9
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN apt-get install -y cron

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt from the project root into the container at /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the DataCollector contents to /app/ and the database folder to /app/database
COPY DataCollector/ .
COPY database/ database/

# Set the file permission for apiCollector.py
RUN chmod +x /app/apiCollector.py

RUN crontab crontab

# Copy start.sh from DataCollector into the Docker image and make it executable
COPY DataCollector/start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
