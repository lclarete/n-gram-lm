#!/bin/bash

# Part 1: collecting data

set -eou pipefail

readonly TRAIN=train.txt
readonly TEST=test.txt


download(){
    curl -- https://data.statmt.org/news-crawl/en/news.2008.en.shuffled.deduped.gz | gunzip -c > "${TRAIN}"
    curl -- https://data.statmt.org/news-crawl/en/news.2009.en.shuffled.deduped.gz | gunzip -c > "${TEST}"
}

download


