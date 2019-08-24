Implementing a simple Web-crawler
=================================

Some days back I took a Python programming course for data analysis. There was an optional assignment to implement a web-crawler.
I was thinking to enhance it. It makes request to https://en.wikipedia.org with the **Special:Random** tag (e.g. https://en.wikipedia.org/wiki/Special:Random). Wikipedia sends a random html page.

After the parsing the same another request is made to the first link in the main-body of the page. It contunies this process until a predetermined page is received. There is a few seconds time gap between each requests.

For each random page it took 20-30 hops to reach the target url "https://en.wikipedia.org/wiki/Philosophy". 10-15 iterations of the main loop was run.

To scale up the crawler programme I felt not to use the wikipedia.org's servers. Using that will slow the app down. Also it will impact the wikipedia and they might block my IP assuming a [denial-of-service attack (DoS attack)](https://en.wikipedia.org/wiki/Denial-of-service_attack "Wikipedia article").

So I have to host a local wikipedia.

I will break down the documentation in two parts-
1. [Host Wikipedia locally](host_wikipedia.md "Host Wikipedia locally").
2. [About the web-crawler application](web_crawler_implementation.md "Web-crawler application").

**Linux(Ubuntu 18 LTS) is used for the work.**

These will be incremental documentation. So there would be further updates.