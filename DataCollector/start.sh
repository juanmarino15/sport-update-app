#!/bin/sh
python /app/apiCollector.py &
service cron start && touch /var/log/cron.log && tail -f /var/log/cron.log
