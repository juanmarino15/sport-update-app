import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.path
from flask import Flask, render_template_string, request
from datetime import datetime,timedelta


from DataAnalyzer import dataAnalyzer  # Import the module

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
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
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tennis Events</title>
            <!-- Link to Bootstrap CSS for styling -->
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h2>Tennis Events Results on {{ yesterday }}</h2>
                <form method="post">
                    <div class="form-group">
                        <label for="country">Country:</label>
                        <input type="text" class="form-control" id="country" name="country">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
                <br>
                {% if message %}
                <div class="alert alert-info">
                    {{ message }}
                </div>
                {% endif %}
                {% if events %}
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
                {% else %}
                    <div class="alert alert-info">
                        No results found for tennis players from {{ country }} on {{ yesterday }}.
                    </div>
                {% endif %}
                <div class="panel panel-default">
                    <div class="panel-heading">Results by Country</div>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Country</th>
                                <th>Total Players</th>
                                <th>Players Who Won</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for country, data in stats.items() %}
                            <tr>
                                <td>{{ country }}</td>
                                <td>{{ data.players }}</td>
                                <td>{{ data.winners }}</td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
    ''', events=events, country=country, yesterday=formatted_yesterday, stats=stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # test
