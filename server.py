""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# Import Section
from flask import Flask, render_template, request, redirect
import requests
from dotenv import load_dotenv
import os
import json

# load all environment variables
load_dotenv()
MS_TEAMS_WEBHOOK = os.getenv("MS_TEAMS_WEBHOOK")

app = Flask(__name__)

##Routes
@app.route('/', methods=['POST'])
def listen_for_meraki_alerts():
    try:
        meraki_alerts = request.get_json()
        print(meraki_alerts)
        headers = { 'Content-Type': 'application/json' }
        payload = {
            "@context": "https://schema.org/extensions",
            "@type": "MessageCard",
            "themeColor": "0072C6",
            "title": "Meraki Alerts",
            "text": f"<pre>Organization: {meraki_alerts['organizationName']}\nNetwork: {meraki_alerts['networkName']}\nDevice: {meraki_alerts['deviceName']}\nAlert: {meraki_alerts['alertType']}\nAlert Level: {meraki_alerts['alertLevel']}\nOccurred At: {meraki_alerts['occurredAt']}</pre>"
        }
        response = requests.request("POST", MS_TEAMS_WEBHOOK, headers=headers, data=json.dumps(payload))
        return "", 200
    except Exception as e:
        print(e)
        return "", 500

#Main Function
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
