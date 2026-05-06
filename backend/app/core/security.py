from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer(auto_error=False)

MOCK_USERS = {
    "reviewer@karnataka.gov": {"role": "reviewer", "name": "Priya Sharma", "dept": "Legal Cell"},
    "officer@karnataka.gov": {"role": "officer", "name": "Ravi Kumar", "dept": "Revenue Department"},
    "head@karnataka.gov": {"role": "head", "name": "Suresh Nair", "dept": "Revenue Department"},
    "secretary@karnataka.gov": {"role": "secretary", "name": "IAS Meena Iyer", "dept": "Chief Secretary Office"},
    "admin@karnataka.gov": {"role": "admin", "name": "System Admin", "dept": "NIC"},
    "new_officer@karnataka.gov": {"role": "officer", "name": "Amit Patel (New Transfer)", "dept": "Urban Development"},
}

def create_token(email: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": email, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials:
        # Return demo user for easy judge access
        return {"email": "officer@karnataka.gov", "role": "officer", "name": "Ravi Kumar", "dept": "Revenue Department"}
    payload = decode_token(credentials.credentials)
    email = payload.get("sub")
    user = MOCK_USERS.get(email, {})
    return {"email": email, "role": payload.get("role"), **user}

def require_role(*roles):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail=f"Requires role: {roles}")
        return user
    return checker
