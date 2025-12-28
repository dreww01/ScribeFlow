import os
import uvicorn
import logging
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("scribeflow")

# Load variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Check for PORT (standard for Cloud Run) and HOST
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on http://{'localhost' if host == '0.0.0.0' else host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
