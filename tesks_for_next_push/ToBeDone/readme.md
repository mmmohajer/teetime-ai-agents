```sh
docker exec -it app-api-1 bash
python manage.py createsuperuser #(mohammad@teetimegolfpass.com)
```

```sh
docker exec -it app-scraper-1 bash
scrapy crawl teetime
```

```sh
docker exec -it app-api-1 bash
fab buildgrouplist
fab addzohodesktodb
fab addzohodesktokb
fab buildpredfinedmessages
```
