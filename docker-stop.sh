#!/bin/bash

# Cook Assistant Docker Stop Script
set -e

echo "🛑 Stopping Cook Assistant..."
echo ""

# Use docker compose (V2) or docker-compose (V1)
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Stop the services
$COMPOSE_CMD down

echo ""
echo "✅ All services stopped successfully!"
echo ""
echo "To start again, run: ./docker-start.sh"
echo "To remove volumes too, run: $COMPOSE_CMD down -v"

