FROM python:3.9
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN apt-get install -y cron

WORKDIR /app

# Copy required files and folders into the Docker container
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
#COPY database/initialize_db.sql /docker-entrypoint-initdb.d/


# Set permissions for the necessary scripts and files
RUN chmod +x /app/DataCollector/apiCollector.py
RUN chmod +x /app/DataCollector/start.sh
#RUN #chmod +x /app/database/initialize_db.py

# Set up the cron job
RUN crontab /app/DataCollector/crontab

# The command that runs when the container starts
CMD ["./DataCollector/start.sh"]
