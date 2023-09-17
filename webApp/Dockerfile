FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt from the project root into the container's WORKDIR
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project into the container's WORKDIR
COPY . .

# Set the working directory to /app/webApp
WORKDIR /app/webApp

CMD ["python", "app.py"]
