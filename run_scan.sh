#!/bin/bash

set -e

echo "🚀 Running Qrypsis Compliance Scan..."

# Default config file
CONFIG_PATH="./config.yaml"

# Allow override via first arg
if [ -n "$1" ]; then
  CONFIG_PATH="$1"
fi

python3 scanner/main.py --config "$CONFIG_PATH"