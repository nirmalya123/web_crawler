#!/bin/bash
set -x

# rm -f Gemfile.lock

jekyll clean

# gem install jekyll -v 3.8.5

# gem install github-pages -v 204

# gem install minima -v 2.5.1

bundle update

bundle update jekyll

bundle update github-pages

bundle update minima

bundle install

bundle exec jekyll serve

