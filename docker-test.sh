#!/bin/bash

# Cook Assistant Docker Test Script
set -e

echo "🧪 Cook Assistant - Docker Setup Verification"
echo "============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Use docker compose (V2) or docker-compose (V1)
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Test counter
PASSED=0
FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Check Docker installation
echo "Test 1: Docker Installation"
if command -v docker &> /dev/null; then
    pass "Docker is installed"
    docker --version
else
    fail "Docker is not installed"
fi
echo ""

# Test 2: Check Docker Compose installation
echo "Test 2: Docker Compose Installation"
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    pass "Docker Compose is installed"
    $COMPOSE_CMD version
else
    fail "Docker Compose is not installed"
fi
echo ""

# Test 3: Check .env file
echo "Test 3: Environment Configuration"
if [ -f .env ]; then
    pass ".env file exists"
    if grep -q "MODAL_API_KEY=" .env && ! grep -q "your_modal_api_key_here" .env; then
        pass "MODAL_API_KEY is configured"
    else
        warn "MODAL_API_KEY might not be properly configured"
    fi
else
    fail ".env file not found"
    warn "Run './docker-start.sh' to create one"
fi
echo ""

# Test 4: Check if services are running
echo "Test 4: Service Status"
if $COMPOSE_CMD ps | grep -q "Up"; then
    pass "Services are running"
    $COMPOSE_CMD ps
else
    warn "Services are not running"
    echo "   Start services with: ./docker-start.sh"
fi
echo ""

# Test 5: Check backend health (only if services are running)
echo "Test 5: Backend Health Check"
if command -v curl &> /dev/null; then
    if curl -s -f http://localhost:8080/health > /dev/null 2>&1; then
        HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
        pass "Backend is healthy"
        echo "   Response: $HEALTH_RESPONSE"
    else
        if $COMPOSE_CMD ps | grep -q "Up"; then
            fail "Backend is not responding"
            echo "   Check logs: ./docker-logs.sh backend"
        else
            warn "Backend is not running"
        fi
    fi
else
    warn "curl is not installed - skipping health check"
fi
echo ""

# Test 6: Check if UI is accessible
echo "Test 6: UI Accessibility"
if curl -s -f http://localhost:8501 > /dev/null 2>&1; then
    pass "UI is accessible at http://localhost:8501"
else
    if $COMPOSE_CMD ps | grep -q "Up"; then
        warn "UI might still be starting up"
        echo "   Wait a few seconds and try: curl http://localhost:8501"
    else
        warn "UI is not running"
    fi
fi
echo ""

# Test 7: Check Docker network
echo "Test 7: Docker Network"
if docker network ls | grep -q "cook-assistant"; then
    pass "Docker network exists"
else
    if $COMPOSE_CMD ps | grep -q "Up"; then
        fail "Docker network not found"
    else
        warn "Docker network not created (services not running)"
    fi
fi
echo ""

# Test 8: Check Docker images
echo "Test 8: Docker Images"
if docker images | grep -q "cook-assistant"; then
    pass "Docker images built"
    docker images | grep "cook-assistant" | head -2
else
    warn "Docker images not found"
    echo "   Build images with: make build"
fi
echo ""

# Test 9: Check file permissions
echo "Test 9: File Permissions"
if [ -x ./docker-start.sh ]; then
    pass "docker-start.sh is executable"
else
    warn "docker-start.sh is not executable"
    echo "   Fix with: chmod +x docker-start.sh"
fi

if [ -x ./docker-stop.sh ]; then
    pass "docker-stop.sh is executable"
else
    warn "docker-stop.sh is not executable"
    echo "   Fix with: chmod +x docker-stop.sh"
fi
echo ""

# Test 10: Check key files
echo "Test 10: Required Files"
for file in Dockerfile docker-compose.yml .dockerignore requirements.txt; do
    if [ -f "$file" ]; then
        pass "$file exists"
    else
        fail "$file is missing"
    fi
done
echo ""

# Summary
echo "============================================="
echo "Test Summary"
echo "============================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✨ All critical tests passed!${NC}"
    echo ""
    echo "🚀 Quick Commands:"
    echo "   Start:    ./docker-start.sh"
    echo "   Stop:     ./docker-stop.sh"
    echo "   Logs:     ./docker-logs.sh"
    echo "   Or use:   make up / make down / make logs"
    echo ""
    echo "🌐 Access Points:"
    echo "   UI:       http://localhost:8501"
    echo "   Backend:  http://localhost:8080"
    echo "   API Docs: http://localhost:8080/docs"
else
    echo -e "${YELLOW}⚠️  Some tests failed. Please review the output above.${NC}"
    echo ""
    echo "📚 For help, see:"
    echo "   - DOCKER_README.md (detailed guide)"
    echo "   - DOCKER_SETUP_SUMMARY.md (setup overview)"
fi
echo ""

