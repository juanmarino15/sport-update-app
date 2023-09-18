import os
import sys
import requests
from flask import Flask, render_template_string, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataAnalyzer import dataAnalyzer

app = Flask(__name__)

TEMPLATE_STRING = '''
<!DOCTYPE html>
<html>
<head>
    <title>Colombian Events</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h2>Colombian Events</h2>
        
        <form method="post">
            <div class="form-group">
                <label for="country">Country:</label>
                <input type="text" class="form-control" id="country" name="country">
            </div>
            <div class="form-group">
                <label for="start_date">Start Date:</label>
                <input type="date" class="form-control" id="start_date" name="start_date">
            </div>
            <div class="form-group">
                <label for="end_date">End Date:</label>
                <input type="date" class="form-control" id="end_date" name="end_date">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <br>
        {% if message %}
        <div class="alert alert-info">
            {{ message }}
        </div>
        {% endif %}
        
        <!-- Displaying the events table -->
        <table class="table table-striped">
            <!-- ... [table headers and rows here] -->
        </table>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def main():
    message = None
    if request.method == "POST":
        country = request.form["country"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        response = requests.post("http://api_collector_host:5001/collect_data", json={
            "country": country,
            "start_date": start_date,
            "end_date": end_date
        })

        api_response = response.json()
        if api_response.get("status") == "success":
            message = api_response.get("message")
        else:
            message = "Failed to start data collection!"

    events = dataAnalyzer.fetch_colombian_events()
    return render_template_string(TEMPLATE_STRING, events=events, message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
