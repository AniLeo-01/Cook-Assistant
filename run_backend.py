#!/usr/bin/env python3
"""
Run the Cook Assistant backend server.

Usage:
    python run_backend.py
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import uvicorn
    from app.backend.config import config
    
    print("🚀 Starting Cook Assistant Backend...")
    print(f"📡 Server will run on http://{config.BACKEND_HOST}:{config.BACKEND_PORT}")
    print(f"🔗 Modal endpoint: {config.MODAL_BASE_URL}")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "app.backend.main:app",
        host=config.BACKEND_HOST,
        port=config.BACKEND_PORT,
        reload=True,
        log_level="info"
    )

