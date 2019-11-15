<H1>Security best practices</H1>
<br>
* Check ls /run/secrets/<br>

```
docker exec -it Container_ID ls /run/secrets/
```

* Check content trust<br>

```
cat /etc/docker/daemon.json | grep content-trust
cat /etc/docker/daemon.json | grep enforced
echo $DOCKER_CONTENT_TRUST
```
