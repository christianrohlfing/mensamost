#!/usr/bin/env python

# Mattermost mensa bot
# Version history
# - 2018-15-02 | First version | rohlfing

import json, urllib.request, requests
import datetime, locale
locale.setlocale(locale.LC_ALL, 'de_DE') # so the date is displayed in German

# Config stuff
mensaid = 187 # openmensa.org id, here Mensa Academica in Aachen
mensaname = 'Mensa Academica'
mattermost_url = "https://servername.com/hooks/somesecret" # url to mattermost webhook
message_footer = '\n[English menu](http://www.studierendenwerk-aachen.de/speiseplaene/academica-w-en.html)\n'# footer to displayed message

# prepare title
message = '---\n#### '+mensaname+', ' + datetime.date.today().strftime("%A, %d.%m.%Y") + '\n\n'

mensaurl = 'https://openmensa.org/api/v2/canteens/'+"{:d}".format(mensaid)+'/days/'+datetime.date.today().strftime("%Y-%m-%d")  +'/meals'

# use openmensa.org for providing the menu
with urllib.request.urlopen(mensaurl) as url:# open url
  data = json.loads(url.read().decode()) # fetch and decode json
  for meal in data: # loop over all meals
    priceStr = ""
    price = meal["prices"]["students"]
    
    # parse price
    if price is not None:        
      priceStr = " (" + "{:.2f}".format(price).replace(".",",") + " €)"
    
    # parse name
    name = meal["name"]
    if name.count(' |') > 0:# replace bars with bold first and then with commata
      name = name.replace(' |','**,',1)
    else:
      name = name + "**"
    name = name.replace(' |',',')
    
    # create formatted message
    message = message + "- " +  meal["category"] + " **" + name + priceStr + "\n"

# end of message
message = message + '\n---'
message = message + message_footer

# provide data
mm_data = {"username": "mensabot", "text": message}

# gogogo!
r = requests.post(mattermost_url, data=json.dumps(mm_data),verify="/etc/ssl/fullchain.pem")
