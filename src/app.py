"""
🚀 CORE AGENT APP (FastAPI Integration)
"""

import os
import sys

# Thêm thư mục gốc vào path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
