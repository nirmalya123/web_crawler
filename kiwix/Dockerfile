FROM alpine:latest

# Or - docker pull kiwix/kiwix-serve

# Install kiwix-serve
WORKDIR /
RUN apk add --no-cache curl bzip2
RUN curl -kL https://download.kiwix.org/release/kiwix-tools/kiwix-tools_linux-x86_64-3.0.1.tar.gz | tar -xz && \
    mv kiwix-tools*/kiwix-serve /usr/local/bin && \
    rm -r kiwix-tools*

# Run kiwix-serve
VOLUME /data
WORKDIR /data
EXPOSE 80

ENTRYPOINT ["/usr/local/bin/kiwix-serve", "--port", "80"]
# ENTRYPOINT ["/usr/local/bin/kiwix-serve", "--port",  "80", "--library", "/library.xml"]

# /media/nirmad/New\ Volume/wikipedia_offline/kiwix/
# wikipedia_en_all_nopic.zim
# wikipedia_en_top_nopic.zim
# wikipedia_en_simple_all_nopic.zim

# Run - docker run -v /media/nirmad/New\ Volume/wikipedia_offline/kiwix:/data -p 8080:80 kiwix_server11 wikipedia_en_simple_all_nopic.zim

# Run - docker run -v /media/nirmad/New\ Volume/wikipedia_offline/kiwix:/data -p 8080:80 kiwix_server11 wikipedia_en_top_nopic.zim

# Run - docker run -v /media/nirmad/New\ Volume/wikipedia_offline/kiwix:/data -p 8080:80 kiwix_server11 wikipedia_en_all_nopic.zim
