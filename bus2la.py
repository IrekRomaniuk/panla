#https://docs.microsoft.com/en-us/python/api/azure-servicebus/azure.servicebus?view=azure-python
from azure.servicebus import QueueClient, Message
from datacollectorapi import client
from datacollectorapi import helper
from ast import literal_eval
import os

# Create the QueueClient
con_string = os.environ['CONNECTION_STRING'].rstrip("\n\r")
queue_name = os.environ['QUEUE_NAME'].rstrip("\n\r")
customer_id = os.environ['CUSTOMER_ID'].rstrip("\n\r")
shared_key = os.environ['SHARED_KEY'].rstrip("\n\r")
log_type = os.environ['LOG_TYPE'].rstrip("\n\r") # 'SyslogTest'
batch_size = int(os.environ['BATCH_SIZE'].rstrip("\n\r"))
batch, batch_size =[], batch_size 
print(con_string , queue_name, customer_id, shared_key, log_type, batch_size)

queue_client = QueueClient.from_connection_string(con_string, queue_name)
api = client.DataCollectorAPIClient(customer_id,shared_key)
while True:
    # Receive the message from the queue
    with queue_client.get_receiver() as queue_receiver:
        #https://docs.microsoft.com/en-us/python/api/azure-servicebus/azure.servicebus.receive_handler.receiver?view=azure-python#fetch-next-max-batch-size-none--timeout-none-
        #https://docs.microsoft.com/en-us/python/api/azure-servicebus/azure.servicebus.common.message.message?view=azure-python
        messages = queue_receiver.fetch_next(timeout=3)
        print("{} messages".format(len(messages)))
        for message in messages:
            message_eval = literal_eval(str(message))
            print(message_eval)
            batch.append(message_eval) #literal_eval()
            message.complete()
            print("batch {}".format(len(batch)))            
            if len(batch) >= batch_size:
                print("SENT {}".format(len(batch)))
                response = api.post_data(log_type, batch)
                print("{}".format(response.status_code))
                batch.clear()
                    
            
                    