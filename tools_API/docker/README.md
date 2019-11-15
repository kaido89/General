<H1>Security best practices</H1>
<br>
1. Check ls /run/secrets/<br>

```
docker exec -it Container_ID ls /run/secrets/
```

2. Check content trust<br>

```
cat /etc/docker/daemon.json | grep content-trust
cat /etc/docker/daemon.json | grep enforced
echo $DOCKER_CONTENT_TRUST
```
