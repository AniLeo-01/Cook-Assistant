#!/bin/bash

# Cook Assistant Docker Logs Viewer
set -e

# Use docker compose (V2) or docker-compose (V1)
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Check if a service name was provided
if [ $# -eq 0 ]; then
    echo "📋 Viewing logs for all services..."
    echo "   Press Ctrl+C to exit"
    echo ""
    $COMPOSE_CMD logs -f
else
    echo "📋 Viewing logs for: $1"
    echo "   Press Ctrl+C to exit"
    echo ""
    $COMPOSE_CMD logs -f "$1"
fi

