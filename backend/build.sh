#!/usr/bin/env bash
set -o errexit
set -o pipefail

# System dependencies
apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt