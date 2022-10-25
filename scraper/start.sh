#! /bin/sh

python -m http.server 8887 &
python scraper.py
