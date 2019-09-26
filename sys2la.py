#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacollectorapi import client
from datacollectorapi import helper
import socketserver, os, json

# Put your customer id and shared key below. For these info, see also
# https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-data-collector-api#sample-requests
HOST, PORT = "0.0.0.0", int(os.environ["SYSLOG_PORT"])
log_type = os.environ['LOG_TYPE'].rstrip("\n\r") # 'SyslogTest'
customer_id = os.environ['CUSTOMER_ID'].rstrip("\n\r")
shared_key = os.environ['SHARED_KEY'].rstrip("\n\r")
fieldnames = ("Type","Subtype","Source","Destination","Port","Application","Action")
# "$type","$subtype","$src","$dst","$dport","$app","$action"
# https://docs.python.org/3/library/socketserver.html
class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(bytes.decode(self.request[0].strip())).split(",")
        socket = self.request[1]
        print( "{0} : {1}".format(self.client_address[0], data))
        json_data=dict(zip(fieldnames, data))
        print( "{0} {1} {2}".format(json_data["Source"],json_data["Destination"],json_data["Port"]))
        #body = json.dumps(json_data)
        #post_data(customer_id, shared_key, body, log_type)  
        api = client.DataCollectorAPIClient(customer_id,shared_key) 
        response = api.post_data(log_type, json_data)
        if (helper.is_success(response.status_code)):
            print( 'Succeeded in posting data to Data Collector API!!')
        else:
            print( "Failure: Error code:{}".format(response.status_code))

if __name__ == '__main__':    
    try:
        print( "Starting: {0} on {1}:{2}".format(log_type, HOST,PORT))
        server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")
