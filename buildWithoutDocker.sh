#!/usr/bin/env bash

for i in $(cat docker/env); do
	export $i
done
pip3 install -U -r requirements.txt --user
python3 src/scraper.py;
