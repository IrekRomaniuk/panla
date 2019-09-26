
## Docker

### sys2la

```
docker build -t sys2la .
docker run -d --name sys2la \
    -e "SYSLOG_PORT=6514" -e "LOG_TYPE=PanLogsTest"  \
    -e "CUSTOMER_ID=$CUSTOMER_ID" -e "SHARED_KEY=$SHARED_KEY" \
    -p 6514:6514/udp \
    sys2la
docker login
docker tag sys2la irom77/sys2la
docker push irom77/sys2la
```

or 

### web2la

```
docker build -t web2la .
docker run -d --name web2la \
    -e "PORT=8514" -e "LOG_TYPE=PanLogsTestB" -e "DEBUG=True" -e "URL=/api" \
    -e "CUSTOMER_ID=$CUSTOMER_ID" -e "SHARED_KEY=$SHARED_KEY" \
    -p 8514:8514/tcp \
    web2la
docker login
docker tag web2la irom77/web2la
docker push irom77/web2la
```
## Testing

## curl

```
curl -d '{"Type":"TEST","Subtype":"subtype","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port","Application":"Application","Action":"Action"}' -H "Content-Type: application/json" -X POST http://localhost:8514/threats

curl -d '{"Type":"TEST","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port"}' -H "Content-Type: application/json" -X POST http://localhost:8514/threats
curl -d '{"Type":"TEST","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port"}' -H "Content-Type: application/json" -X POST http://10.4.1.99:8514/threats
```

### locustio

```
locust --host=http://10.4.1.99:8514 --locustfile web2la_test.py

locust --host=http://10.4.1.99:8514 -f web2la_test.py --no-web -c 10 -r 1000 -t 300s --only-summary

docker@ubuntu-home:~$ /home/docker/.local/bin/locust --host=http://10.4.1.99:8514 -f ./web2py_test.py --no-web -c 10 -r 1000 -t 300s --only-summary

```


### k8s

```
kubectl scale --replicas=3 deployment/web2la
```