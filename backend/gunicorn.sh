#!/bin/sh
gunicorn foodgram.wsgi:application --bind 0:8000