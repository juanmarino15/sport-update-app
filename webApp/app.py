import os
import sys
from flask import Flask, render_template_string, request, Response
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Summary, Counter, generate_latest, CONTENT_TYPE_LATEST

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.path
from DataAnalyzer import dataAnalyzer  # Import the module

app = Flask(__name__)

# Define your Prometheus metrics
REQUEST_TIME = Summary('webapp_request_processing_seconds', 'Time spent processing main requests')
REQUEST_COUNT = Counter('webapp_request_count', 'Total main requests processed')

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

@app.route("/", methods=["GET", "POST"])
@REQUEST_TIME.time()
def main():
    REQUEST_COUNT.inc()
    yesterday = datetime.now() - timedelta(1)
    formatted_yesterday = yesterday.strftime('%Y-%m-%d')

    if request.method == "POST":
        country = request.form.get("country")
        events = dataAnalyzer.fetch_tennis_events(country)
    else:
        country = "Colombia"  # Default country
        events = dataAnalyzer.fetch_tennis_events()

    stats = dataAnalyzer.country_statistics()

    return render_template_string('''
        <!-- your previous HTML template -->
    ''', events=events, country=country, yesterday=formatted_yesterday, stats=stats)

if __name__ == "__main__":
    start_http_server(8000)  # Start Prometheus client server
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
