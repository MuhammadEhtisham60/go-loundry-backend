#!/usr/bin/env bash
# build.sh — Render build script for GoLaundry backend
# Runs during the build phase on Render before the service starts.
set -o errexit

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Collect static files (WhiteNoise will serve them)
python manage.py collectstatic --no-input

# 3. Apply any pending database migrations
python manage.py migrate
