import os
import sys
from flask import Flask, render_template_string, request
from datetime import datetime
from DataAnalyzer import dataAnalyzer  # Import the module

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        country = request.form.get("country")
        events = dataAnalyzer.fetch_tennis_events(country)
    else:
        country = "Colombia"  # Default country
        events = dataAnalyzer.fetch_tennis_events()

    current_date = datetime.now().strftime('%Y-%m-%d')

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
                <h2>Tennis Events</h2>
                <form method="post">
                    <div class="form-group">
                        <label for="country">Country:</label>
                        <input type="text" class="form-control" id="country" name="country" value="{{ country }}">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
                <br>
                {% if events %}
                    <table class="table table-striped">
                        <!-- Table header remains the same... -->
                        <!-- Table body remains the same... -->
                    </table>
                {% else %}
                    <div class="alert alert-info">
                        No results found for {{ country }} on {{ current_date }}.
                    </div>
                {% endif %}
            </div>
        </body>
        </html>
    ''', events=events, country=country, current_date=current_date)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
