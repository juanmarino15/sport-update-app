# Sports Update App

An app that summarizes all daily tennis singles results by country and players. This is the MVP, further iterations will include more sports.
Below are the instructions to run the test files. Everything else is directly running from Heroku and deployed through GithubActions.
Link to the app : https://sports-update-app-49388c1c7601.herokuapp.com/

## Infrastructure
The application employs Docker to manage four distinct services: the Data Collector, Data Analyzer, Web App, and Database. It's orchestrated to ensure smooth data flow and processing, as detailed below:

Data Collection: Initiated by the Data Collector, it polls an API for fresh data and subsequently feeds it into the Heroku Postgres DB. This service operates on a set schedule, waking up via the Heroku Scheduler every day at 5 am for data gathering.

Data Processing: Post data collection, the Data Analyzer refines and formats the data to make it easily consumable by the Web App.

Deployment: The application is auto-deployed to Heroku via GitHub Actions. For deployment specifics, see the .github directory. Note: You'll need to configure environment variables in GitHub Actions if redeploying as a new app.

Metrics Monitoring: Prometheus is utilized for basic metrics collection from an endpoint. While graphical representations aren't currently implemented, you can observe metric variations by making repeated requests.

Remember to properly set up environment variables and other configurations if you plan to repurpose or expand upon this infrastructure.

# Considerations

Make sure you have Python installed. Preferably 3.8+

##  Regarding the rubric
Below is the rubric for A Level Work with all the pointers of where the rubrics are met throughout the project

-Web application basic form, reporting --> Application served on https://sports-update-app-49388c1c7601.herokuapp.com/

-Data collection --> Refer to DataCollector directory

Data analyzer --> Refer to DataAnalyzer directory

Unit tests --> Refer to each test directory under every root directory. Below are the tests you can run locally if you want to double check

Data persistence any data store --> Storing the data in Heroku Postgres DB

Rest collaboration internal or API endpoint --> Collecting data from http://api.sportradar.us API. Refer to data collector for more details

Product environment --> Application currently hosted in Heroku for production

Integration tests --> refer to tests/test_integrationTest.py

Using mock objects or any test doubles --> refer to the test files. Most of them use mock objects for the testing scenarios

Continuous integration --> Currently using github actions. Refer to .github/workflows/actions.yml to get details on deployment and tests ran before the deployment

Production monitoring instrumenting --> Currently using prometheus to collect metrics. Check https://sports-update-app-49388c1c7601.herokuapp.com/metrics

Event collaboration messaging --> Using a simple queue approach where we update a table in the db when datacollector is collecting, then update again once is done. No other job will run until dataCollector finishes collecting data.

Continuous delivery --> Currently using github actions. Refer to .github/workflows/actions.yml to get details on deployment

## Set up

1.  Create virtual environment

    ```shell
    python -m venv venv
    source venv/bin/activate
    ```

1.  Installed required packages
    ```shell
    pip install -r requirements.txt
    ```

## Run Tests

1.  Integration test
    ```shell
    python tests/test_integrationTest.py
    ```

2.  DataCollector Test
    ```shell
    python datacollector/tests/test_apiCollector.py
    ```
    
3.  DataAnalyzer Test
    ```shell
    python dataanalyzer/tests/test_dataAnalyzer.py
    ```

4.  webApp Test
    ```shell
    python webApp/tests/test_webApp.py
    ```
