import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

API_SECRET_TOKEN = os.getenv("API_SECRET_TOKEN")
security = HTTPBearer()

async def get_current_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not API_SECRET_TOKEN or credentials.credentials != API_SECRET_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
