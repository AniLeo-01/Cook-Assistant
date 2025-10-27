#!/bin/bash

# Cook Assistant - Unified Run Script
# Supports both Docker and native Python execution

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
MODE="${1:-auto}"  # auto, docker, native, prod, dev

print_banner() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🍳 Cook Assistant${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

check_docker() {
    if command -v docker &> /dev/null && docker info &> /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

check_python() {
    if command -v python3 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

check_env_file() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env file not found. Creating from example...${NC}"
        cat > .env << 'EOF'
# Cook Assistant Environment Variables
MODAL_API_KEY=your_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
CORS_ORIGINS=*
BACKEND_URL=http://localhost:8080
EOF
        echo -e "${GREEN}✅ Created .env file. Please update MODAL_API_KEY.${NC}"
        echo ""
    fi
}

run_docker_dev() {
    echo -e "${BLUE}🐳 Starting with Docker (Development Mode)...${NC}"
    echo ""
    
    check_env_file
    
    # Export development environment variables
    export MOUNT_SOURCE=1
    export DEBUG=true
    export LOG_LEVEL=debug
    export BACKEND_COMMAND="uvicorn app.backend.main:app --host 0.0.0.0 --port 8080 --reload --log-level debug"
    export RESTART_POLICY=no
    
    echo "📦 Building images..."
    docker compose build
    
    echo ""
    echo "🚀 Starting services..."
    docker compose up
}

run_docker_prod() {
    echo -e "${BLUE}🐳 Starting with Docker (Production Mode)...${NC}"
    echo ""
    
    check_env_file
    
    # Export production environment variables
    export MOUNT_SOURCE=""
    export DEBUG=false
    export LOG_LEVEL=info
    export BACKEND_COMMAND="gunicorn app.backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --access-logfile - --error-logfile - --log-level info"
    export RESTART_POLICY=always
    export STREAMLIT_EXTRA_ARGS="--server.enableCORS=false --server.enableXsrfProtection=true"
    
    echo "📦 Building images..."
    docker compose build
    
    echo ""
    echo "🚀 Starting services in detached mode..."
    docker compose up -d
    
    echo ""
    echo -e "${GREEN}✅ Services started!${NC}"
    echo ""
    echo "📊 View logs: docker compose logs -f"
    echo "🛑 Stop services: docker compose down"
}

run_docker() {
    echo -e "${BLUE}🐳 Starting with Docker...${NC}"
    echo ""
    
    check_env_file
    
    # Export default environment variables
    export MOUNT_SOURCE=1
    export DEBUG=false
    export LOG_LEVEL=info
    export RESTART_POLICY=unless-stopped
    
    echo "📦 Building images..."
    docker compose build
    
    echo ""
    echo "🚀 Starting services..."
    docker compose up -d
    
    echo ""
    echo -e "${GREEN}✅ Services started!${NC}"
    echo ""
    echo "📊 View logs: docker compose logs -f"
    echo "🛑 Stop services: docker compose down"
}

run_native() {
    echo -e "${BLUE}🐍 Starting with Native Python...${NC}"
    echo ""
    
    if ! check_python; then
        echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.10 or higher.${NC}"
        exit 1
    fi
    
    # Check dependencies
    echo "📦 Checking dependencies..."
    if ! python3 -c "import fastapi" 2>/dev/null; then
        echo "📥 Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    echo -e "${GREEN}✅ Dependencies OK${NC}"
    echo ""
    
    # Start backend in background
    echo "🚀 Starting backend server..."
    python3 run_backend.py &
    BACKEND_PID=$!
    
    # Wait for backend to start
    echo "⏳ Waiting for backend to initialize..."
    sleep 3
    
    # Start UI
    echo "🎨 Starting UI server..."
    python3 run_ui.py &
    UI_PID=$!
    
    echo ""
    echo -e "${GREEN}✅ Cook Assistant is running!${NC}"
    echo ""
    echo "📡 Backend API: http://localhost:8080"
    echo "🌐 Streamlit UI: http://localhost:8501"
    echo ""
    echo "Press CTRL+C to stop all servers"
    echo ""
    
    # Wait for interrupt
    trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $UI_PID 2>/dev/null; echo '✅ Done!'; exit 0" INT
    
    # Keep script running
    wait
}

show_help() {
    print_banner
    echo "Usage: ./run.sh [mode]"
    echo ""
    echo "Modes:"
    echo "  auto      Automatically detect and use Docker if available, otherwise native (default)"
    echo "  docker    Use Docker Compose (default settings)"
    echo "  dev       Use Docker Compose with development settings (hot-reload, debug)"
    echo "  prod      Use Docker Compose with production settings (optimized, no mounts)"
    echo "  native    Run directly with Python (no Docker)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh              # Auto-detect best method"
    echo "  ./run.sh docker       # Use Docker with default settings"
    echo "  ./run.sh dev          # Development mode with hot-reload"
    echo "  ./run.sh prod         # Production mode"
    echo "  ./run.sh native       # Native Python execution"
    echo ""
    echo "Docker Commands:"
    echo "  docker compose logs -f      # View logs"
    echo "  docker compose down         # Stop services"
    echo "  docker compose restart      # Restart services"
    echo ""
    echo "Access Points:"
    echo "  Frontend:    http://localhost:8501"
    echo "  Backend:     http://localhost:8080"
    echo "  API Docs:    http://localhost:8080/docs"
    echo ""
}

# Main execution
print_banner

case "$MODE" in
    auto)
        if check_docker; then
            run_docker
        else
            echo -e "${YELLOW}⚠️  Docker not available. Falling back to native Python.${NC}"
            echo ""
            run_native
        fi
        ;;
    docker)
        if ! check_docker; then
            echo -e "${RED}❌ Docker is not available.${NC}"
            echo "Please install Docker or run with: ./run.sh native"
            exit 1
        fi
        run_docker
        ;;
    dev)
        if ! check_docker; then
            echo -e "${RED}❌ Docker is not available.${NC}"
            echo "Please install Docker or run with: ./run.sh native"
            exit 1
        fi
        run_docker_dev
        ;;
    prod)
        if ! check_docker; then
            echo -e "${RED}❌ Docker is not available.${NC}"
            exit 1
        fi
        run_docker_prod
        ;;
    native)
        run_native
        ;;
    help|--help|-h)
        show_help
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Unknown mode: $MODE${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

