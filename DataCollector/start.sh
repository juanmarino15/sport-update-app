#!/bin/sh
python /app/database/initialize_db.py

python /app/DataCollector/apiCollector.py &
service cron start && touch /var/log/cron.log && tail -f /var/log/cron.log
