#!/usr/bin/env python3
"""
Run the Streamlit UI for Cook Assistant.

Usage:
    python run_ui.py
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import subprocess
    
    UI_FILE = Path(__file__).parent / "src" / "app" / "ui" / "streamlit_app.py"
    
    print("🎨 Starting Cook Assistant UI (Streamlit)...")
    print(f"🌐 The app will open in your browser automatically")
    print("Press CTRL+C to stop the server\n")
    
    # Run streamlit
    subprocess.run([
        "streamlit", "run",
        str(UI_FILE),
        "--server.port=8501",
        "--server.headless=false",
        "--browser.gatherUsageStats=false"
    ])

