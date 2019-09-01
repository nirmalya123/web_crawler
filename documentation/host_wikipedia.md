Host Wikipedia Locally
======================

> **Update on 27th August 2019**
>
> Using the below steps importing the 70GB wiki XML-dump file was slow in the system. I seemed like it would take months to import all the articles. So I had to look for alternatives. Fortunately [kiwix](https://www.kiwix.org/en/) provided the solution that served my purpose. Details are on [this page](kiwix_steps.md).

#### Prerequisite
Sufficient HDD space. The downloaded dump file is nearly 16GB. After uncompressing it is approximately 70GB.

## There are two main parts-
1. How to get the article pages in the Wikipedia.
2. How to host it.

How to get the article pages in the Wikipedia
---------------------------------------------

Wikipedia shares free copies of all available content to interested users. These databases can be used for offline and personal use. (Ref. https://en.wikipedia.org/wiki/Wikipedia:Database_download)

#### Useful links
1. It provides useful links for Wikimedia - https://dumps.wikimedia.org/
2. Useful infomation about working with the dump - https://meta.wikimedia.org/wiki/Data_dumps

#### Download the dump
1. Got to https://dumps.wikimedia.org/enwiki/latest/ (Ref. https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia)

2. Download [enwiki-latest-pages-articles.xml.bz2](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2).
Use a download manager. The file more than 16GB. There are other versions as well. One can download as per their need. As the name suggests this file is for English language and is latest [multistream](https://en.wikipedia.org/wiki/Wikipedia:Database_download#Should_I_get_multistream? "Wikipedia - Should I get multistream?") as on the date.

3. Extract the zip file in a folder.


Host the Wikipedia
------------------
[Mediawiki](https://www.mediawiki.org/wiki/MediaWiki "Mediawiki Website") is used to host the wikipedia. It is also the popular one.

I decided to user Docker containers. It would help me to keep my workstation clean and modular. (Ref. https://www.mediawiki.org/wiki/Docker)


### Setup mediawiki docker

#### Setup docker

Very good initial and overall guide for docker - https://docs.docker.com/get-started/.
You may also refer to [this](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04).

#### Docker compose file

1. Refer to my docker compose file [here](https://github.com/nirmalya123/web_crawler/blob/master/host_wiki/stack.yml "Github link") . Also refer to https://hub.docker.com/_/mediawiki as well. My folder structure is as below-
```
└── host_wiki
	├── LocalSettings.php
	└── stack.yml
```
Initially the `LocalSettings.php` file will not be there. It would be available after the setup is complete.
> Comment the line `- ./LocalSettings.php:/var/www/html/LocalSettings.php` for initial run.

2. The unzipped dump file was placed at `/media/nirmad/New Volume/wikipedia_offline/mediawiki_store`. I used an external HDD for it. Also created `/media/nirmad/New Volume/wikipedia_offline/db` for the database.

I faced some inconsitent issue while using `mysql` image hence sticked to the `mariadb`. The `mysql` container was not able to run consistently.
> Also note the `MYSQL_ROOT_PASSWORD` set here. It would be needed at the time of setting up the database for Mediawiki.

3. Now initialize the docker swarm

```
sudo docker swarm init
```

Sample output-
```
Swarm initialized: current node (8pyipi9aawwzntnogkqi15f81) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-3g21ufuxnu2lecxrmor83qp7hj6xijrptqlcj7ppa9jbca5g54-4va1u9f734m65a62lk0n8ooa3 192.168.1.3:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

4. Initialize the stack
```
sudo docker stack deploy -c stack.yml mediawiki
```

Smple output-
```
Ignoring unsupported options: links, restart

Creating network mediawiki_default
Creating service mediawiki_mediawiki
Creating service mediawiki_database
```

5. Some useful diagnostic to check

Check the stack status-
```
sudo docker stack ls
```
Output-
```
NAME                SERVICES            ORCHESTRATOR
mediawiki           2                   Swarm
```
Check the mediawiki task-

```
sudo docker stack services mediawiki
```
Output-
```
ID                  NAME                  MODE                REPLICAS            IMAGE               PORTS
xv81zw80gdlx        mediawiki_mediawiki   replicated          1/1                 mediawiki:latest    *:8080->80/tcp
yo14p4fco3qz        mediawiki_database    replicated          1/1                 mariadb:latest
```
Check the container details-
```
sudo docker container ls
```
Output-
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
868320e8a647        mariadb:latest      "docker-entrypoint.s…"   13 seconds ago      Up 10 seconds       3306/tcp            mediawiki_database.1.umodg2menj31gcfuoaznr5k
fe76b0a3a594        mediawiki:latest    "docker-php-entrypoi…"   34 seconds ago      Up 31 seconds       80/tcp              mediawiki_mediawiki.1.w9dzwjf8b90sbcsm4k5p295
```
Also inspect the tasks. (You may note down the IP addresses.)
```
sudo docker inspect mediawiki_database
sudo docker inspect mediawiki_mediawiki
```

If anything goes as not expected you may use these commands.
| Purpose | Command |
| ------------- |-------------|
| Tear down the application | `sudo docker stack rm mediawiki` |
| Remove the swarm | `sudo docker swarm leave --force`|
| Remove all containers | `sudo docker container prune` |
| Remove all docker networking | `sudo docker network prune` |

#### Setup Mediawiki and the database

Once the contianers are up open http://localhost:8080 in a browser. If any specific IP-address was used in the `swarm init` then use that one.

Configuration pages and steps are as below-

1. **Page 1** Just continue.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page1.jpg?raw=true "Mediawiki installation - Page 1")

2. **Page 2** If the below text is visible then continue.
> The environment has been checked. You can install MediaWiki

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page2.jpg?raw=true "Mediawiki installation - Page 2")

3. **Page 3** This page is important.
- Database type should be `MariaDB` here.
- Datebase host should be the **_service name_** as in the docker-compose file. It should not be _localhost_. The container are running inside swam and each containers will be assigned different IP addresses as per the docker networking components.
- Database password should be the one specified in the docker-compose file.
- Rest of the fields should not be altered.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page3.jpg?raw=true "Mediawiki installation - Page 3")

4. **Page 4** Just continue.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page4.jpg?raw=true "Mediawiki installation - Page 4")

5. **Page 5** Specify the `Name of wiki`, `Username` and `Password`. You may complete the isntalltion here or can configure further.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page5.jpg?raw=true "Mediawiki installation - Page 5")

6. **Page 6** Configure and continue. In my case nothing was altered.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page6.jpg?raw=true "Mediawiki installation - Page 6")

7. **Page 7** Just continue.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page7.jpg?raw=true "Mediawiki installation - Page 7")

8. **Page 8** Check if all the points are showing **Done**. Else restart installtion.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page8.jpg?raw=true "Mediawiki installation - Page 8")

9. **Page 9** It would show `Complete!`.
> Make sure to donwload the `LocalSettings.php` file. To the same location of the docker-compose file.

![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_install_page9.jpg?raw=true "Mediawiki installation - Page 9")

**Restart the containers**
Run the below commands
1. Teardown the run environment
```
sudo docker stack rm mediawiki
sudo docker swarm leave --force
```

2. Uncomment the line `- ./LocalSettings.php:/var/www/html/LocalSettings.php` in the dokcer-compose file and save.

3. Start the enviroment
```
sudo docker swarm init
sudo docker stack deploy -c stack.yml mediawiki
```

#### Import the dump in Mediawiki

1. Login to the Mediawiki continer
```
sudo docker exec  -it fe76b0a3a594 bash
```
The prompt will be `root@fe76b0a3a594:/var/www/html#`

2. Import
```
php maintenance/importDump.php images/enwiki-latest-pages-articles-multistream.xml
```
Sample output-
```
100 (0.73 pages/sec 0.73 revs/sec)
200 (0.62 pages/sec 0.62 revs/sec)
300 (0.55 pages/sec 0.55 revs/sec)
400 (0.54 pages/sec 0.54 revs/sec)
500 (0.52 pages/sec 0.52 revs/sec)
600 (0.52 pages/sec 0.52 revs/sec)
700 (0.53 pages/sec 0.53 revs/sec)
800 (0.52 pages/sec 0.52 revs/sec)
900 (0.51 pages/sec 0.51 revs/sec)
1000 (0.51 pages/sec 0.51 revs/sec)
...
```

3. While the import is in progress you can access http://localhost:8080/index.php/Special:Random to see if any wikipedia content is visible.
Sample-
![Alt text](https://github.com/nirmalya123/web_crawler/blob/master/documentation/mediawiki_page.jpg?raw=true "MediaWiki Special:Random")
It is a very lenghty process.