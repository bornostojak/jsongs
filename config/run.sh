#!/bin/sh

gunicorn -w 3 -b 0.0.0.0:$PORT jsongs:app --access-logfile -
