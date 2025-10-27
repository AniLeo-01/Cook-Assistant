.PHONY: help build up down restart logs logs-backend logs-ui clean status shell-backend shell-ui test

# Default target
help:
	@echo "Cook Assistant - Docker Commands"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - View logs (all services)"
	@echo "  make logs-backend  - View backend logs"
	@echo "  make logs-ui       - View UI logs"
	@echo "  make status        - Show service status"
	@echo "  make shell-backend - Open shell in backend container"
	@echo "  make shell-ui      - Open shell in UI container"
	@echo "  make clean         - Stop services and remove volumes"
	@echo "  make dev           - Start in development mode"
	@echo "  make prod          - Start in production mode"
	@echo ""

# Detect docker compose command
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

# Build images
build:
	@echo "🏗️  Building Docker images..."
	$(DOCKER_COMPOSE) build

# Start services
up:
	@echo "🚀 Starting Cook Assistant..."
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "📡 Backend API:   http://localhost:8080"
	@echo "🌐 Streamlit UI:  http://localhost:8501"
	@echo ""

# Stop services
down:
	@echo "🛑 Stopping Cook Assistant..."
	$(DOCKER_COMPOSE) down
	@echo "✅ Services stopped!"

# Restart services
restart:
	@echo "🔄 Restarting services..."
	$(DOCKER_COMPOSE) restart
	@echo "✅ Services restarted!"

# View all logs
logs:
	$(DOCKER_COMPOSE) logs -f

# View backend logs
logs-backend:
	$(DOCKER_COMPOSE) logs -f backend

# View UI logs
logs-ui:
	$(DOCKER_COMPOSE) logs -f ui

# Show service status
status:
	@echo "📊 Service Status:"
	@echo ""
	$(DOCKER_COMPOSE) ps

# Open shell in backend container
shell-backend:
	$(DOCKER_COMPOSE) exec backend bash

# Open shell in UI container
shell-ui:
	$(DOCKER_COMPOSE) exec ui bash

# Clean everything
clean:
	@echo "🧹 Cleaning up..."
	$(DOCKER_COMPOSE) down -v
	@echo "✅ Cleanup complete!"

# Development mode
dev:
	@echo "🔧 Starting in development mode..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up

# Production mode
prod:
	@echo "🚀 Starting in production mode..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✅ Production services started!"

# Rebuild and start
rebuild:
	@echo "🏗️  Rebuilding and starting..."
	$(DOCKER_COMPOSE) up -d --build
	@echo "✅ Rebuild complete!"

# View help
info:
	@echo ""
	@echo "📡 Backend API:   http://localhost:8080"
	@echo "📚 API Docs:      http://localhost:8080/docs"
	@echo "🌐 Streamlit UI:  http://localhost:8501"
	@echo ""

