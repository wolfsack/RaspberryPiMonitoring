#!/bin/bash

pip3 install -r requirements.txt

waitress-serve --listen=*:5000 wsgi:app

# bash run.sh