#!/bin/sh
sudo docker container run -d --name mediawiki -p 8080:80 mediawiki

sudo docker container run -d --name mediawiki-mysql -v mediawiki-mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=admin11 mysql

sudo docker network create mediawiki

sudo docker network connect mediawiki mediawiki

sudo docker network connect mediawiki mediawiki-mysql

