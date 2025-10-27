"""
Cook Assistant - Streamlit UI

A modern web interface for the Cook Assistant AI.
"""

import streamlit as st
import requests
from typing import List, Optional
import json
import os

# Configuration
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

# Page configuration
st.set_page_config(
    page_title="Cook Assistant",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .ingredient-tag {
        display: inline-block;
        background: linear-gradient(135deg, #4ecdc4, #ff6b6b);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-weight: 500;
    }
    .recipe-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .recipe-content {
        background: white;
        color: #2d3436;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    .assistant-message {
        background: #f7f9fc;
        color: #2d3436;
        margin-right: 2rem;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-healthy {
        background-color: #00b894;
    }
    .status-error {
        background-color: #d63031;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'generated_recipe' not in st.session_state:
    st.session_state.generated_recipe = None

# Helper functions
def check_backend_health() -> dict:
    """Check if the backend is healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.ok:
            return {"status": "healthy", "data": response.json()}
        else:
            return {"status": "error", "message": "Backend returned an error"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def generate_recipe(ingredients: List[str], additional_instructions: Optional[str] = None) -> dict:
    """Generate a recipe from ingredients."""
    try:
        payload = {
            "ingredients": ingredients,
            "additional_instructions": additional_instructions,
            "temperature": 1.0,
            "max_tokens": 1024
        }
        response = requests.post(
            f"{API_BASE_URL}/generate-recipe",
            json=payload,
            timeout=60
        )
        if response.ok:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def send_chat_message(message: str, conversation_history: List[dict]) -> dict:
    """Send a chat message to the assistant."""
    try:
        payload = {
            "message": message,
            "conversation_history": conversation_history,
            "temperature": 1.0
        }
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=60
        )
        if response.ok:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

# Header
st.markdown("""
<div class="main-header">
    <h1>👨‍🍳 Cook Assistant</h1>
    <p>Transform your ingredients into delicious recipes with AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Backend Status
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Backend health check
    health = check_backend_health()
    if health["status"] == "healthy":
        st.markdown(
            '<div><span class="status-indicator status-healthy"></span>'
            '<strong>Backend:</strong> Connected</div>',
            unsafe_allow_html=True
        )
        if "data" in health and "available_models" in health["data"]:
            st.caption(f"Model: {health['data']['available_models'][0]}")
    else:
        st.markdown(
            '<div><span class="status-indicator status-error"></span>'
            '<strong>Backend:</strong> Disconnected</div>',
            unsafe_allow_html=True
        )
        st.error("⚠️ Backend is not running. Start it with: `python run_backend.py`")
    
    st.divider()
    
    st.subheader("📖 About")
    st.info("""
    **Cook Assistant** uses AI to help you:
    - Generate recipes from ingredients
    - Get cooking advice and tips
    - Learn cooking techniques
    - Find ingredient substitutions
    """)
    
    st.divider()
    
    st.subheader("🔗 API Endpoints")
    st.code(API_BASE_URL, language=None)
    if st.button("🔄 Refresh Connection"):
        st.rerun()

# Main content - Tabs
tab1, tab2 = st.tabs(["🍽️ Recipe Generator", "💬 Chat Assistant"])

# Tab 1: Recipe Generator
with tab1:
    st.header("What's in your kitchen?")
    st.write("Enter your ingredients and let AI create a delicious recipe for you")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ingredient_input = st.text_input(
            "Add an ingredient",
            placeholder="e.g., eggs, chicken, tomatoes",
            key="ingredient_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("➕ Add Ingredient"):
            if ingredient_input and ingredient_input.strip():
                ingredient = ingredient_input.strip().lower()
                if ingredient not in st.session_state.ingredients:
                    st.session_state.ingredients.append(ingredient)
                    st.rerun()
    
    # Display ingredients
    if st.session_state.ingredients:
        st.subheader("Your Ingredients")
        
        # Create columns for ingredient tags
        cols = st.columns(5)
        for idx, ingredient in enumerate(st.session_state.ingredients):
            with cols[idx % 5]:
                if st.button(f"❌ {ingredient}", key=f"remove_{ingredient}"):
                    st.session_state.ingredients.remove(ingredient)
                    st.rerun()
        
        st.divider()
        
        # Additional instructions
        additional_instructions = st.text_area(
            "Additional Instructions (Optional)",
            placeholder="e.g., make it vegetarian, low-carb, spicy, etc.",
            height=100
        )
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate Recipe", type="primary", use_container_width=True):
                with st.spinner("🔮 Generating your recipe..."):
                    result = generate_recipe(
                        st.session_state.ingredients,
                        additional_instructions if additional_instructions else None
                    )
                    
                    if result["status"] == "success":
                        st.session_state.generated_recipe = result["data"]
                        st.success("✅ Recipe generated successfully!")
                    else:
                        st.error(f"❌ Error: {result['message']}")
        
        # Display recipe
        if st.session_state.generated_recipe:
            st.divider()
            
            recipe_data = st.session_state.generated_recipe
            
            st.markdown("""
            <div class="recipe-box">
                <h2>🍳 Your Recipe</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="recipe-content">
                {recipe_data['recipe']}
            </div>
            """, unsafe_allow_html=True)
            
            st.caption(f"**Ingredients used:** {', '.join(recipe_data['ingredients_used'])}")
            
            # Clear recipe button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🗑️ Clear Recipe & Start Over", use_container_width=True):
                    st.session_state.generated_recipe = None
                    st.session_state.ingredients = []
                    st.rerun()
    else:
        st.info("👆 Start by adding some ingredients above")

# Tab 2: Chat Assistant
with tab2:
    st.header("Chat with Cook Assistant")
    st.write("Ask me anything about cooking, recipes, or techniques!")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        # Initial message if no chat history
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-message assistant-message">
                <strong>👨‍🍳 Cook Assistant</strong><br><br>
                Hello! I'm your cooking assistant. Ask me anything about recipes, cooking techniques, 
                ingredient substitutions, or general cooking advice!
            </div>
            """, unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You</strong><br><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>👨‍🍳 Cook Assistant</strong><br><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.divider()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        chat_input = st.text_input(
            "Your message",
            placeholder="Ask me anything about cooking...",
            key="chat_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        send_button = st.button("📤 Send", use_container_width=True)
    
    if send_button and chat_input:
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": chat_input
        })
        
        # Send to backend
        with st.spinner("🤔 Thinking..."):
            result = send_chat_message(chat_input, st.session_state.conversation_history)
            
            if result["status"] == "success":
                assistant_response = result["data"]["response"]
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
                # Update conversation history for context
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": chat_input
                })
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
                st.rerun()
            else:
                st.error(f"❌ Error: {result['message']}")
    
    # Clear chat button
    if st.session_state.chat_history:
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.conversation_history = []
                st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #636e72; padding: 2rem 0;">
    <p>Powered by AI • Built with Streamlit • Made with ❤️</p>
</div>
""", unsafe_allow_html=True)

