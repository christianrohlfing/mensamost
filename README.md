# mensamost
Mattermost bot for daily posts of mensa lunch menu

- Fetches lunch menu from openmensa.org
- Publishes markdown-formatted message to a Mattermost webhook

## Installation
### Ubuntu 

Run `sudo crontab -e` and add the following entry
``` 
11 11 * * 1,2,3,4,5 python3 /path/to/mensamost/mensamost.py >/dev/null 2>&1
```

This cron job is executed every workday (1-5) at 11:11 am.
