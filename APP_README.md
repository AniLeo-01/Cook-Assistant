# Cook Assistant - Setup Guide

Welcome to Cook Assistant! This guide will help you set up and run the application.

## 🏗️ Architecture

The application consists of three main components:

1. **Modal Deployment** - LLM model served via Modal (already deployed)
2. **Backend API** - FastAPI server that communicates with the Modal endpoint
3. **Streamlit UI** - Modern interactive web interface built with Streamlit

## 📋 Prerequisites

- Python 3.10 or higher
- Modal account with deployed model
- Internet connection

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root (optional, defaults are already set):

```env
MODAL_API_KEY=2is0Irr9q7
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
```

### 3. Start the Backend

Open a terminal and run:

```bash
python run_backend.py
```

The backend will start on `http://localhost:8080`

You should see:
```
🚀 Starting Cook Assistant Backend...
📡 Server will run on http://0.0.0.0:8080
🔗 Modal endpoint: https://v-ibe--cook-assistant-v1-serve.modal.run/v1
```

### 4. Start the UI

Open another terminal and run:

```bash
python run_ui.py
```

The Streamlit UI will start on `http://localhost:8501` and automatically open in your browser.

## 🎯 Features

### 🍽️ Recipe Generator Tab
- Add ingredients with a simple input field
- Remove ingredients with one click
- Add optional instructions (e.g., "make it vegetarian", "low-carb")
- Generate AI-powered recipes instantly
- Beautiful, easy-to-read recipe format with styling
- Clear and start over functionality

### 💬 Chat Assistant Tab
- Interactive chat interface with message history
- Ask cooking questions and get expert advice
- Get cooking tips and techniques
- Learn about ingredient substitutions
- Conversation context maintained throughout session
- Clear chat history option

## 🔧 API Endpoints

The backend provides the following endpoints:

- `GET /` - API information
- `GET /health` - Health check and connection status
- `POST /generate-recipe` - Generate a recipe from ingredients
- `POST /chat` - Chat with the cooking assistant

### Example API Usage

#### Generate Recipe

```bash
curl -X POST http://localhost:8080/generate-recipe \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": ["eggs", "milk", "flour", "sugar"],
    "additional_instructions": "make it vegetarian"
  }'
```

#### Chat

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I make scrambled eggs?"
  }'
```

## 📁 Project Structure

```
Cook-Assistant/
├── src/
│   ├── app/
│   │   ├── backend/
│   │   │   ├── __init__.py
│   │   │   ├── main.py          # FastAPI application
│   │   │   └── config.py        # Configuration management
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   └── streamlit_app.py # Streamlit UI application
│   │   └── modal_deploy.py      # Modal deployment script
├── run_backend.py               # Backend runner
├── run_ui.py                    # Streamlit UI runner
├── start_app.sh                 # One-command startup (Unix/Mac)
├── start_app.bat                # One-command startup (Windows)
├── requirements.txt             # Python dependencies
├── APP_README.md                # This file
├── STREAMLIT_README.md          # Detailed Streamlit guide
└── .env                         # Environment variables (optional)
```

## 🔍 Troubleshooting

### Backend won't start
- Check if port 8080 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check the Modal endpoint is accessible

### Streamlit UI can't connect to backend
- Ensure the backend is running on port 8080
- Check the sidebar for connection status
- Click "Refresh Connection" button in sidebar
- Verify CORS is properly configured

### Modal endpoint errors
- Verify the Modal API key is correct
- Check if the Modal deployment is running
- Test the endpoint directly: `curl https://v-ibe--cook-assistant-v1-serve.modal.run/v1/health`

## 🛠️ Development

### Running in Development Mode

The backend automatically runs with hot-reload enabled. Any changes to Python files will trigger a restart.

Streamlit also auto-reloads when you save changes to `streamlit_app.py`.

### Modifying the UI

Edit `src/app/ui/streamlit_app.py`:
- Modify layouts and components using Streamlit APIs
- Update CSS in the `st.markdown()` section for custom styling
- Add new tabs or features using `st.tabs()`
- Streamlit automatically reloads on file save

### Changing the Modal Endpoint

Update the base URL in `src/app/backend/config.py`:

```python
MODAL_BASE_URL = "your-modal-endpoint-here"
```

Or set it in your `.env` file:

```env
MODAL_BASE_URL=your-modal-endpoint-here
```

## 📝 Notes

- The Modal API key is hardcoded for development. In production, use environment variables and Modal Secrets.
- The UI runs on a simple HTTP server suitable for development only.
- For production deployment, consider using:
  - Nginx or Apache for serving the UI
  - Gunicorn or similar for the FastAPI backend
  - Proper authentication and rate limiting

## 🎨 Streamlit UI Features

- **Modern Design** - Beautiful gradient backgrounds and custom styling
- **Responsive Layout** - Works on desktop, tablet, and mobile devices
- **Real-time Updates** - Instant feedback with spinners and status indicators
- **Session State** - Maintains your data while you navigate between tabs
- **Backend Status** - Live connection monitoring in sidebar
- **Interactive Components** - Buttons, text inputs, and chat interface
- **Tab Navigation** - Easy switching between Recipe Generator and Chat

## 🤝 Contributing

To add new features:

1. Backend: Add endpoints in `src/app/backend/main.py`
2. Frontend: Update `src/app/ui/streamlit_app.py` to call new endpoints
3. Styling: Modify the CSS in the `st.markdown()` section of `streamlit_app.py`

For more detailed Streamlit information, see `STREAMLIT_README.md`.

## 📄 License

This project is part of the Cook Assistant application.

---

Enjoy cooking with AI! 👨‍🍳✨

