from locust import HttpLocust, TaskSet, task
import json

#locust --host=http://10.4.1.99:8514 --locustfile web2la_test.py 
#locust --host=http://10.4.1.99:8514 -f web2la_test.py --no-web -c 10 -r 1000 -t 300s --only-summary
class UserBehavior(TaskSet):
 
    @task(1)    
    def create_post(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/threats",data= json.dumps({
      "Type": "TESTPERFAZURE",
      "Source": "E11.222.111.222",
      "Destination": "E22.111.222.111",
      "Port": "12345"
    }), 
    headers=headers, 
    name = "Post a log entry")
 
 
class WebsiteUser(HttpLocust):
    min_wait = 0
    max_wait = 0
    task_set = UserBehavior
    #host = "http://10.4.1.99:8514"
