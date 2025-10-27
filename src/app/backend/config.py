"""Configuration management for the Cook Assistant backend."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Modal API Configuration
    MODAL_API_KEY = os.getenv("MODAL_API_KEY")
    MODAL_BASE_URL = "https://v-ibe--cook-assistant-v1-serve.modal.run/v1"
    
    # Server Configuration
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8080"))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Model Configuration
    DEFAULT_TEMPERATURE = 1.0
    DEFAULT_MAX_TOKENS = 8192
    DEFAULT_SEED = 48

config = Config()

