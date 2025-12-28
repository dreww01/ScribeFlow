import os
import uvicorn
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Check for both PORT and port, default to 8080
    port_val = os.environ.get("PORT") or os.environ.get("port") or 8080
    port = int(port_val)
    
    print(f"Starting server on port {port}...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
