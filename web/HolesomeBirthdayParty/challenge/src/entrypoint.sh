#!/bin/sh
gunicorn -w 4 --bind 0.0.0.0:1337 server:app