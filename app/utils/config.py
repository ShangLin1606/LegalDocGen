from pathlib import Path
from dotenv import load_dotenv
import os
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LOCAL_TINYLLAMA_PATH = os.getenv("LOCAL_TINYLLAMA_PATH", "./models/tinyllama")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(ROOT / "data/chroma"))
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", str(ROOT / "mlruns"))
