all:
	$(warning "make startmysql, startredis, strartapp, start, stopmysql, stopredis, stopapp, stop, restart")

runmysql:
	docker run --name mysqldb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=django_template -v /tmp/mysql/data/:/var/lib/mysql  -d mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

runredis:
	docker run --name redisdb -v /tmp/redis/data:/data -d redis

runapp:
	docker run --name django_template_app -v /Users/kangxin/Program/py3pro/djangotemplate/:/home/docker/code/ --link mysqldb:mysqld --link redisdb:redisdb -p 7000:8000 -d kagxin/django_template


startmysql:
	docker start mysqldb

startredis:
	docker start redisdb

strartapp:
	docker start django_template_app


stopmysql:
	docker stop mysqldb
stopredis:
	docker stop redisdb
stopapp:
	docker stop django_template_app


migrate:
# 	docker exec -it django_template_app "python3 /home/docker/code/manage.py migrate"

run:
	$(MAKE) runmysql
	$(MAKE) runmysql
	$(MAKE) runmysql

start:
	$(MAKE) startmysql
	$(MAKE) startredis
	$(MAKE) strartapp

stop:
	$(MAKE) stopmysql
	$(MAKE) stopredis
	$(MAKE) stopapp

restart:
	$(MAKE) stop
	$(MAKE) start

rmc:
	docker rm mysqldb
	docker rm redisdb
	docker rm django_template_app

clean:
	$(MAKE) stop
	docker rm mysqldb
	docker rm redisdb
	docker rm django_template_app