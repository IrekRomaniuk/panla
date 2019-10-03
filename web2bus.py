#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.servicebus import QueueClient, Message
from flask import Flask, request
import os, json

# Put your customer id and shared key below. For these info, see also
# https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-data-collector-api#sample-requests
HOST, PORT, DEBUG, URL = "0.0.0.0", int(os.environ["PORT"]), os.environ['DEBUG'].rstrip("\n\r"), os.environ['URL'].rstrip("\n\r")
con_string = os.environ['CONNECTION_STRING'].rstrip("\n\r")
queue_name = os.environ['QUEUE_NAME'].rstrip("\n\r")
app = Flask(__name__)
# Create the QueueClient
queue_client = QueueClient.from_connection_string(con_string, queue_name)
@app.route(URL, methods=['GET', 'POST']) #, methods=['POST']) #GET requests will be blocked
def handle():
    if request.is_json:
        req_data = request.get_json()
        # Send a test message to the queue
        msg = Message(req_data)
        res=queue_client.send(msg)
        return "{}".format(res) 
    else:
        return "{}".format("Request is not JSON")         

if __name__ == '__main__': 
    print("{0} {1}".format(queue_name, con_string)) 
    app.run(HOST, debug=DEBUG, port=PORT) #threaded=True
