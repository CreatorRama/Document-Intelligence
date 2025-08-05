#!/usr/bin/env bash
set -o errexit

# Install system dependencies for psycopg
apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc

# Install Python packages
pip install -r requirements.txt