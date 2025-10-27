# 🍳 Cook Assistant

An AI-powered cooking assistant that helps you create recipes, answer cooking questions, and generate personalized meal suggestions using advanced language models.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

## 📖 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
  - [Docker Deployment (Recommended)](#docker-deployment-recommended)
  - [Native Installation](#native-installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

- **🤖 AI-Powered Recipe Generation** - Create custom recipes from available ingredients
- **💬 Interactive Chat Assistant** - Ask cooking questions and get expert advice
- **🎯 Smart Ingredient Analysis** - Extract and analyze ingredients from recipes
- **📝 Recipe Summarization** - Get concise summaries of complex recipes
- **🚀 Modern Web UI** - Beautiful, responsive Streamlit interface with gradient styling
- **⚡ Fast API Backend** - High-performance FastAPI backend with Modal integration
- **🐳 Docker Ready** - One-command deployment with Docker Compose
- **🔄 Hot Reload** - Development mode with automatic code reloading

## 🏗️ Architecture

The application consists of three main components:

```
┌─────────────────────────────────────────┐
│   User Browser                          │
└───────────────┬─────────────────────────┘
                │
                │ http://localhost:8501
                │
┌───────────────▼─────────────────────────┐
│   Streamlit UI (Frontend)               │
│   - Recipe Generator                    │
│   - Chat Assistant                      │
│   - Real-time updates                   │
└───────────────┬─────────────────────────┘
                │
                │ http://localhost:8080
                │
┌───────────────▼─────────────────────────┐
│   FastAPI Backend                       │
│   - Recipe generation API               │
│   - Chat API                            │
│   - Health monitoring                   │
└───────────────┬─────────────────────────┘
                │
                │ HTTPS
                │
┌───────────────▼─────────────────────────┐
│   Modal AI Service (vLLM)               │
│   - LLM inference                       │
│   - Model: anileo1/cook-assistant       │
│   - GPU acceleration                    │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Using the Unified Run Script (Easiest)

The simplest way to run Cook Assistant:

```bash
# Clone the repository
git clone https://github.com/yourusername/Cook-Assistant.git
cd Cook-Assistant

# Run with auto-detection (uses Docker if available, otherwise native Python)
./run.sh

# Or specify mode explicitly:
./run.sh docker    # Use Docker (default settings)
./run.sh dev       # Development mode (hot-reload, debug)
./run.sh prod      # Production mode (optimized)
./run.sh native    # Native Python (no Docker)
```

**Access Points:**
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs

### Docker Deployment (Recommended)

#### Prerequisites
- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Modal API Key

#### Steps

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/Cook-Assistant.git
   cd Cook-Assistant
   
   # Create .env file (or let run.sh create it)
   echo "MODAL_API_KEY=your_api_key_here" > .env
   ```

2. **Run the application**
   ```bash
   # Auto-start with Docker
   ./run.sh docker
   
   # Or manually with docker compose
   docker compose up -d
   ```

3. **Manage services**
   ```bash
   # View logs
   docker compose logs -f
   
   # Stop services
   docker compose down
   
   # Restart
   docker compose restart
   ```

#### Development vs Production

```bash
# Development mode (hot-reload, source mounted)
./run.sh dev

# Production mode (optimized, no mounts, Gunicorn)
./run.sh prod
```

### Native Installation (Without Docker)

#### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Modal API key ([Get one here](https://modal.com))

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Cook-Assistant.git
   cd Cook-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional - run.sh creates .env automatically)
   ```bash
   echo "MODAL_API_KEY=your_api_key_here" > .env
   ```

4. **Start the application**
   ```bash
   # Use the unified run script
   ./run.sh native
   
   # Or manually (two terminals):
   # Terminal 1:
   python run_backend.py
   
   # Terminal 2:
   python run_ui.py
   ```

5. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8080
   - API Docs: http://localhost:8080/docs

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MODAL_API_KEY` | Modal API authentication key | - | Yes |
| `BACKEND_HOST` | Backend server host | `0.0.0.0` | No |
| `BACKEND_PORT` | Backend server port | `8080` | No |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `*` | No |
| `BACKEND_URL` | Backend URL for UI connection | `http://localhost:8080` | No |

### Model Configuration

The application uses a fine-tuned model deployed on Modal:
- **Model:** `anileo1/cook-assistant-Qwen3-0.6B`
- **Endpoint:** `https://v-ibe--cook-assistant-v1-serve.modal.run/v1`
- **GPU:** T4 (configurable in `src/app/modal_deploy.py`)
- **Max Tokens:** 8192
- **Default Temperature:** 1.0

To modify the model configuration, edit `src/app/backend/config.py` and `src/app/modal_deploy.py`.

## 📡 API Documentation

### Endpoints

#### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "modal_connection": "connected",
  "available_models": ["anileo1/cook-assistant-Qwen3-0.6B"]
}
```

#### Generate Recipe
```bash
POST /generate-recipe
Content-Type: application/json

{
  "ingredients": ["eggs", "milk", "flour", "sugar"],
  "additional_instructions": "make it vegetarian",
  "temperature": 1.0,
  "max_tokens": 1024
}

Response:
{
  "recipe": "Recipe title and instructions...",
  "ingredients_used": ["eggs", "milk", "flour", "sugar"],
  "model": "anileo1/cook-assistant-Qwen3-0.6B"
}
```

#### Chat
```bash
POST /chat
Content-Type: application/json

{
  "message": "How do I make scrambled eggs?",
  "conversation_history": [],
  "temperature": 1.0
}

Response:
{
  "response": "To make scrambled eggs...",
  "model": "anileo1/cook-assistant-Qwen3-0.6B"
}
```

### Interactive API Documentation

Visit http://localhost:8080/docs for the full interactive Swagger UI documentation.

### Example API Usage

#### Using cURL
```bash
# Generate a recipe
curl -X POST http://localhost:8080/generate-recipe \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": ["chicken", "rice", "vegetables"],
    "additional_instructions": "make it spicy"
  }'

# Chat with assistant
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the best way to cook rice?"
  }'
```

#### Using Python
```python
import requests

# Generate recipe
response = requests.post(
    "http://localhost:8080/generate-recipe",
    json={
        "ingredients": ["chicken", "rice", "vegetables"],
        "additional_instructions": "make it spicy"
    }
)
print(response.json())

# Chat
response = requests.post(
    "http://localhost:8080/chat",
    json={"message": "How do I boil pasta?"}
)
print(response.json())
```

## 💻 Development

### Project Structure

```
Cook-Assistant/
├── src/
│   ├── app/
│   │   ├── backend/
│   │   │   ├── main.py              # FastAPI application
│   │   │   └── config.py            # Configuration management
│   │   ├── ui/
│   │   │   └── streamlit_app.py     # Streamlit frontend
│   │   ├── modal_deploy.py          # Modal deployment script
│   │   ├── data_pipeline.py         # Data processing pipeline
│   │   ├── finetuner.py             # Model fine-tuning
│   │   └── llm.py                   # LLM integration utilities
│   ├── prompts/
│   │   └── dataset_prompts.py       # Prompt templates
│   ├── utils/
│   │   ├── data_generators.py       # Dataset generators
│   │   ├── io_utils.py              # I/O utilities
│   │   └── model_utils.py           # Model utilities
│   └── notebooks/                   # Jupyter notebooks
├── dataset/
│   ├── processed/                   # Processed datasets
│   │   ├── recipe_generation_dataset.json
│   │   ├── ingredient_extraction_dataset.json
│   │   └── ...
│   ├── RecipeNLG_dataset.csv        # Source dataset
│   └── recipes.json                 # Raw recipes
├── docker-compose.yml               # Docker orchestration (unified)
├── Dockerfile                       # Docker image definition
├── Makefile                         # Make commands
├── run.sh                           # Unified run script (Docker + native)
├── docker-logs.sh                   # View Docker logs
├── docker-stop.sh                   # Stop Docker services
├── docker-test.sh                   # Test Docker setup
├── requirements.txt                 # Python dependencies
├── requirements-prod.txt            # Production dependencies
├── run_backend.py                   # Backend runner script
├── run_ui.py                        # UI runner script
└── README.md                        # This file
```

### Running in Development Mode

```bash
# Development mode with Docker (hot-reload, source mounted)
./run.sh dev

# Or manually:
export MOUNT_SOURCE=1
export DEBUG=true
export LOG_LEVEL=debug
docker compose up
```

Both backend and frontend support hot-reloading:
- **Backend:** Uvicorn auto-reloads on file changes
- **Frontend:** Streamlit auto-reloads on file changes

Native development (without Docker):
```bash
# Terminal 1 - Backend with hot-reload
python run_backend.py

# Terminal 2 - Frontend with hot-reload
python run_ui.py
```

### Data Pipeline

Process recipes and create training datasets:

```bash
# Run data pipeline
python -m src.app.data_pipeline

# Fine-tune model
python -m src.app.finetuner

# Test model inference
python src/app/tests/openai_infer.py
```

Datasets are stored in `dataset/` with processed versions in `dataset/processed/`.

### Modal Deployment

Deploy or update the model on Modal:

```bash
# Login to Modal
modal setup

# Deploy the model
modal deploy src/app/modal_deploy.py

# Test the deployment
python src/app/tests/openai_infer.py
```

## 🚢 Deployment

### Production Docker Deployment

```bash
# Production mode (Gunicorn, optimized, no volume mounts)
./run.sh prod

# Or manually:
export MOUNT_SOURCE=""
export DEBUG=false
export LOG_LEVEL=info
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Production Considerations

1. **Environment Variables**
   - Use proper secrets management (e.g., Docker secrets, Kubernetes secrets)
   - Never commit `.env` file with real credentials
   - Rotate API keys regularly

2. **Resource Limits**
   Resource limits are configured via environment variables in `docker-compose.yml`:
   ```bash
   export BACKEND_CPU_LIMIT=2.0
   export BACKEND_MEM_LIMIT=2G
   export UI_CPU_LIMIT=1.0
   export UI_MEM_LIMIT=1G
   docker compose up -d
   ```

3. **Reverse Proxy with HTTPS**
   Use nginx or Traefik for SSL termination. Example nginx configuration:
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8501;
       }
   }
   ```

4. **Monitoring and Logging**
   - Set up log aggregation (e.g., ELK stack)
   - Monitor API performance and errors
   - Set up health check endpoints

5. **Scaling**
   ```bash
   # Scale backend replicas
   docker compose up -d --scale backend=3
   ```

### Manual Production Deployment

```bash
# Install production dependencies
pip install -r requirements-prod.txt

# Run backend with Gunicorn
gunicorn src.app.backend.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8080

# Run Streamlit
streamlit run src/app/ui/streamlit_app.py \
  --server.port=8501 \
  --server.headless=true
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend won't start
```bash
# Check if port is already in use
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or change the port in .env
echo "BACKEND_PORT=8081" >> .env
```

#### 2. Frontend can't connect to backend
- Ensure backend is running: `curl http://localhost:8080/health`
- Check sidebar status indicator in Streamlit UI
- Verify `BACKEND_URL` in `.env` is correct
- Click "Refresh Connection" button in sidebar

#### 3. Modal API errors
```bash
# Verify API key
echo $MODAL_API_KEY

# Test Modal endpoint directly
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://v-ibe--cook-assistant-v1-serve.modal.run/v1/models

# Check Modal deployment status
modal app list
```

#### 4. Docker issues
```bash
# View logs
docker compose logs -f

# Restart services
docker compose restart

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up -d

# Or use the unified script
./run.sh docker
```

#### 5. Missing dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# In Docker
docker-compose build --no-cache
```

#### 6. Port already in use
```bash
# Find what's using the port
lsof -i :8080  # Backend
lsof -i :8501  # Frontend

# Kill the process or change ports in docker-compose.yml
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export LOG_LEVEL=debug

# Run backend
python run_backend.py

# Or in Docker
docker-compose run --rm -e LOG_LEVEL=debug backend python run_backend.py
```

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow PEP 8 style guide
   - Add tests for new features
   - Update documentation
4. **Run tests and linting**
   ```bash
   pytest
   black src/
   flake8 src/
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines

- Write clear, descriptive commit messages
- Add docstrings to all functions and classes
- Include type hints where applicable
- Write tests for new functionality
- Update README.md if adding new features

## 🛠️ Technologies Used

- **Backend:** FastAPI, Uvicorn, Python 3.10+
- **Frontend:** Streamlit
- **AI/ML:** Modal, vLLM, OpenAI API
- **Model:** Qwen3-0.6B fine-tuned on RecipeNLG dataset
- **Data Processing:** Pandas, NumPy
- **Containerization:** Docker, Docker Compose
- **Development:** pytest, black, flake8, mypy

## 📊 Dataset

The model is fine-tuned on processed RecipeNLG dataset:
- **Source:** RecipeNLG (Recipe Natural Language Generation)
- **Processed Datasets:** 
  - Recipe generation
  - Ingredient extraction
  - Recipe summarization
  - Constraint-based generation
  - QA pairs
  - Instruction tuning

Datasets are available in `dataset/processed/`.

## 🙏 Acknowledgments

- Recipe data from [RecipeNLG dataset](https://recipenlg.cs.put.poznan.pl/)
- Powered by [Modal](https://modal.com) for serverless GPU inference
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/)
- Model based on [Qwen3-0.6B](https://huggingface.co/Qwen)


Made with ❤️ by the AniLeo-01

**Happy Cooking! 👨‍🍳✨**
