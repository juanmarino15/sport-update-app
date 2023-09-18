import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.path
from flask import Flask, render_template_string

# Assuming the data analyzer is in the same directory or accessible in the sys.path
from DataAnalyzer import dataAnalyzer  # Import the module

app = Flask(__name__)

@app.route("/")
def main():
    events = dataAnalyzer.fetch_colombian_events()
    print(events)
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
                <h2>Colombian Events</h2>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Event ID</th>
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
                                <td>{{ event.event_id }}</td>
                                <td>{{ event.start_time }}</td>
                                <td>{{ event.competition }}</td>
                                <td>{{ event.round }}</td>
                                <td>{{ event.competitor_1.name }} ({{ event.competitor_1.country }})</td>
                                <td>{{ event.competitor_2.name }} ({{ event.competitor_2.country }})</td>
                                <td>{{ event.scores }}</td>
                                <td>{{ "Competitor 1" if event.flag == "home" else "Competitor 2" }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    ''', events=events)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
