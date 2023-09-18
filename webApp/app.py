import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.path
from flask import Flask, render_template_string,request

# Assuming the data analyzer is in the same directory or accessible in the sys.path
from DataAnalyzer import dataAnalyzer  # Import the module

app = Flask(__name__)

@app.route("/")
def main():
    events = dataAnalyzer.fetch_colombian_events()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Colombian Events</title>
            <!-- Link to Bootstrap CSS for styling -->
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2>Tennis Events</h2>
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
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Start Time</th>
                            <th>Competition</th>
                            <th>Round</th>
                            <th>Competitor 1</th>
                            <th>Competitor 2</th>
                            <th>Scores</th>
                            <th>Winner</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for event in events %}
                            <tr>
                                <td>{{ event.start_time }}</td>
                                <td>{{ event.competition }}</td>
                                <td>{{ event.round }}</td>
                                <td>{{ event.competitor_1.name }} ({{ event.competitor_1.country }})</td>
                                <td>{{ event.competitor_2.name }} ({{ event.competitor_2.country }})</td>
                                <td>{{ event.scores }}</td>
                                <td>{{ "Competitor 1" if event.flag == "Competitors_1_qualifier" else "Competitor 2" }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    ''', events=events)
@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    country = request.form.get("country")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Start the data collection process (pseudo code)
    # e.g. start_data_collection(country, start_date, end_date)

    return f"Data collection started for {country} from {start_date} to {end_date}. Please wait while we process your request."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
