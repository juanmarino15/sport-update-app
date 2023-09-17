FROM python:3.9
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

# Copy required files and folders into the Docker container
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# If you have any scripts or files specific to DataAnalyzer that need permissions set:
RUN chmod +x /app/DataAnalyzer/dataAnalyzer.py


# The command that runs when the container starts
CMD ["./DataAnalyzer/dataAnalyzer.py"]
