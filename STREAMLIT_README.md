# Cook Assistant - Streamlit UI Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Application

#### Option A: One Command (Recommended)

**On Mac/Linux:**
```bash
./start_app.sh
```

**On Windows:**
```
start_app.bat
```

#### Option B: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Streamlit UI:**
```bash
python run_ui.py
```

## 🌐 Access Points

- **Streamlit UI**: http://localhost:8501 (opens automatically)
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs

## ✨ Features

### 🍽️ Recipe Generator Tab
- Add ingredients using the input field
- Remove ingredients by clicking the ❌ button
- Add optional instructions (e.g., "make it vegetarian", "low-carb")
- Click "Generate Recipe" to get AI-powered recipes
- View your recipe in a beautiful formatted display
- Clear and start over anytime

### 💬 Chat Assistant Tab
- Interactive chat interface
- Ask cooking questions and get expert advice
- Conversation history maintained during session
- Topics include:
  - Cooking techniques
  - Ingredient substitutions
  - Recipe modifications
  - General cooking tips

## 🎨 UI Features

- **Modern Design**: Beautiful gradients and clean layout
- **Status Indicator**: Real-time backend connection status in sidebar
- **Responsive**: Works on all screen sizes
- **Session State**: Maintains your data while browsing
- **Error Handling**: Clear error messages and guidance

## 📊 Sidebar Information

The sidebar displays:
- ✅ Backend connection status
- 🤖 Current AI model in use
- 📖 About section
- 🔗 API endpoint information
- 🔄 Refresh connection button

## 💡 Tips

1. **Backend First**: Always start the backend before the UI
2. **Check Status**: Use the sidebar to verify backend connection
3. **Session Persistence**: Your ingredients and chat history are maintained during your session
4. **Multiple Ingredients**: Add as many ingredients as you like
5. **Be Specific**: More detailed instructions lead to better recipes

## 🔧 Troubleshooting

### "Backend: Disconnected" in sidebar
- Make sure the backend is running: `python run_backend.py`
- Check if port 8080 is available
- Verify the Modal endpoint is accessible

### Streamlit won't start
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8501 is available
- Try running directly: `streamlit run src/app/ui/streamlit_app.py`

### Recipes not generating
- Check the backend logs for errors
- Verify your Modal API key is correct
- Ensure the Modal deployment is active

## 🛠️ Development

### File Structure
```
src/app/ui/
└── streamlit_app.py    # Main Streamlit application
```

### Customization

**Change Ports:**
Edit `run_ui.py` and modify:
```python
"--server.port=8501",  # Change this port
```

**Modify Styling:**
Edit the CSS in the `st.markdown()` section of `streamlit_app.py`

**Change API URL:**
Edit `API_BASE_URL` in `streamlit_app.py`:
```python
API_BASE_URL = "http://localhost:8080"
```

## 📝 Streamlit-Specific Features

- **Session State**: Maintains ingredients and chat history
- **Auto-refresh**: Updates UI when data changes
- **Tabs**: Easy navigation between Recipe Generator and Chat
- **Real-time Updates**: Live backend status checking
- **Clean URLs**: No complex routing needed

## 🎯 Next Steps

1. Try generating a recipe with 3-5 ingredients
2. Ask the chat assistant about cooking techniques
3. Experiment with different instructions and preferences
4. Save your favorite recipes for later reference

## 📄 Configuration

Streamlit settings can be customized in `.streamlit/config.toml` (create if needed):

```toml
[server]
port = 8501
headless = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7f9fc"
textColor = "#2d3436"
```

---

Enjoy cooking with AI and Streamlit! 👨‍🍳✨

