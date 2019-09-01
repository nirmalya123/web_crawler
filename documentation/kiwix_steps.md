Hosting Wikipedia using kiwix-serve
===================================

> This documentation is a continuation of [this page](host_wikipedia.md).

[kiwix](https://www.kiwix.org/en/) is a fantastic utility to use Wikipedia and serveral other websites offline. There are serveral mode like an app, hotspot and a server. For my purpose the server mode the apt. The server mode comes as part of kiwix-tools.

#### References
> https://wiki.kiwix.org/wiki/Content_in_all_languages


There are two main steps.
1. Download the dump file. It's in **.zim** format.
2. Run the kiwix-serve.

## Download the dump files
List of the available websites can be found at https://download.kiwix.org/zim/.

The one I downloaded is http://download.kiwix.org/zim/wikipedia_en_all_nopic.zim.

**nopic** means no picture or images. There are other versions(viz. **novid** means no video but with pictures, etc.)

You need to place this file in the docker volume.

**Below is a list of other such stuff**

| Website | Files | Date | Size |
| ------- | ----- | ---- | ---- |
| [wiktionary](https://download.kiwix.org/zim/wiktionary/) | wiktionary_en_all_nopic_2017-08.zim | 2017-08-22 20:39 | 1.4G |
| |wiktionary_en_all_novid_2018-06.zim | 2018-06-25 14:55 | 4.1G |
| [gutenberg](https://download.kiwix.org/zim/gutenberg/) | gutenberg_en_all_2018-07.zim | 2018-07-16 05:17 | 53G |
| |gutenberg_en_all_2018-10.zim | 2018-10-23 07:33 | 53G |
| [wikibooks](https://download.kiwix.org/zim/wikibooks/?C=S;O=D)| wikibooks_en_all_novid_2019-07.zim | 2019-07-24 15:06 | 3.7G |
| | wikibooks_en_all_nopic_2019-07.zim | 2019-07-24 15:14 | 2.7G |
| [wikipedia](https://download.kiwix.org/zim/wikipedia/?C=S;O=D)| wikipedia_en_all_novid_2018-10.zim | 2018-11-06 12:43 | 78G |
| | wikipedia_en_all_novid_2018-06.zim | 2018-07-18 21:21 | 77G |
| | wikipedia_en_movies_2019-07.zim | 2019-07-09 21:12 | 55G |
| | **wikipedia_en_all_nopic_2018-09.zim** | 2018-09-26 16:43 | **35G** |

## Setup the kiwix-serve
I am using a containered approach. The Dockerfile I used is [here](../kiwix/Dockerfile).
The Docker image provided by kiwix is https://hub.docker.com/r/kiwix/kiwix-serve

## Run the kiwix-serve
To run the docker image you can use the below command.
```
sudo docker run -v /media/nirmad/New\ Volume/wikipedia_offline/kiwix:/data -p 8080:80 kiwix_server11 wikipedia_en_all_nopic.zim
```

The file ` wikipedia_en_all_nopic.zim` is at the volume location `/media/nirmad/New\ Volume/wikipedia_offline/kiwix`.


The site URL is `http://localhost:8080/wikipedia_en_all_nopic/A/`

The random wiki page URL is `http://localhost:8080/random?content=wikipedia_en_all_nopic`

### A few observations
The `Philosophy` article was easily reachable for `https://en.wikipedia.org/wiki/Special:Random`. But this was not reachable using the same algorithm for the kiwix-serve. So I had to add some other target articles in the list.