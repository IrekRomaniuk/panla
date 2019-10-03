
## Docker

### web2la

```
docker build -t web2la .
docker run -d --name web2la \
    -e "PORT=8514" -e "LOG_TYPE=PanLogsTestC" -e "DEBUG=True" -e "URL=/api" \
    -e "CUSTOMER_ID=$CUSTOMER_ID" -e "SHARED_KEY=$SHARED_KEY" -e "WINDOW=3" \
    -p 8514:8514/tcp \
    web2la
docker login
docker tag web2la irom77/web2la
docker push irom77/web2la

### web2bus

```
docker build -t web2bus .
docker run -d --name web2bus \
    -e "PORT=9514" -e "QUEUE_NAME=panlogs" -e "DEBUG=True" -e "URL=/api" \
    -e "CONNECTION_STRING=$CONNECTION_STRING" \
    -p 9514:9514/tcp \
    web2bus
docker login
docker tag web2la irom77/web2la
docker push irom77/web2la
```
## Kubernetes

```
kubectl apply -f k8s_web2la.yaml
kubectl scale --replicas=3 deployment/web2la

```

## Testing

## curl
e
```
curl -d '{"Type":"TEST","Subtype":"subtype","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port","Application":"Application","Action":"Action"}' -H "Content-Type: application/json" -X POST http://localhost:8514/api

curl -d '{"Type":"TESTA1","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port"}' -H "Content-Type: application/json" -X POST http://localhost:8514/api
curl -d '{"Type":"TESTA2","Source":"1.1.1.1","Destination":"1.1.1.2","Port":"Port"}' -H "Content-Type: application/json" -X POST http://localhost:9514/api
```

### locustio

```
locust --host=http://10.4.1.99:8514 --locustfile web2la_test.py

locust --host=http://10.4.1.99:8514 -f web2la_test.py --no-web -c 10 -r 1000 -t 300s --only-summary

docker@ubuntu-home:~$ /home/docker/.local/bin/locust --host=http://10.4.1.99:8514 -f ./web2py_test.py --no-web -c 10 -r 1000 -t 300s --only-summary

```
