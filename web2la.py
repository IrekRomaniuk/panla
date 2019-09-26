#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacollectorapi import client
from datacollectorapi import helper
from flask import Flask, request
import os, json

# Put your customer id and shared key below. For these info, see also
# https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-data-collector-api#sample-requests
HOST, PORT, DEBUG, URL = "0.0.0.0", int(os.environ["PORT"]), os.environ['DEBUG'].rstrip("\n\r"), os.environ['URL'].rstrip("\n\r")
log_type = os.environ['LOG_TYPE'].rstrip("\n\r") # 'SyslogTest'
customer_id = os.environ['CUSTOMER_ID'].rstrip("\n\r")
shared_key = os.environ['SHARED_KEY'].rstrip("\n\r")
#fieldnames = ("Type","Subtype","Source","Destination","Port","Application","Action")
app = Flask(__name__)
api = client.DataCollectorAPIClient(customer_id,shared_key)
@app.route('/threats', methods=['GET', 'POST']) #, methods=['POST']) #GET requests will be blocked
def handle_threats():
    if request.is_json:
        req_data = request.get_json()
        #print("{}".format(req_data))
        #print("{0} {1} {2}".format(req_data["Source"],req_data["Destination"],req_data["Port"]))
        response = api.post_data(log_type, req_data)
        #print("Status code: {}".format(response.status_code))
        return "{}".format(response.status_code)
    else:
        return "{}".format("Request is not JSON")    
@app.route(URL, methods=['GET', 'POST']) #, methods=['POST']) #GET requests will be blocked
def handle():
    if request.is_json:
        req_data = request.get_json()
        response = api.post_data(log_type, req_data)
        return "{}".format(response.status_code)
    else:
        return "{}".format("Request is not JSON")         

if __name__ == '__main__': 
    print("{0} {1} {2}".format(log_type, customer_id, shared_key)) 
    app.run(HOST, debug=DEBUG, port=PORT)
