#!/bin/sh

flask db upgrade


exe gunicorn --bind 0.0.0.0:80 "app:create_app()"