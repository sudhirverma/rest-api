#!/bin/sh

flask db upgrade


exex gunicorn --bind 0.0.0.0:80 "app:create_app()"