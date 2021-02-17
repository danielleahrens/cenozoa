#!/bin/bash

gunicorn --bind 0.0.0.0:5000 wsgi:app --log-level info & python alert_engine.py
