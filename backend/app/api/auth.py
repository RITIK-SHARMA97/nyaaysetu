from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_token, MOCK_USERS

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = MOCK_USERS.get(req.email)
    if not user:
        raise HTTPException(status_code=401, detail=f"User not found. Try: officer@karnataka.gov")
    token = create_token(req.email, user["role"])
    return TokenResponse(access_token=token, user={"email": req.email, **user})

@router.get("/users")
def list_demo_users():
    """Show all demo users for easy testing."""
    return [{"email": k, **v} for k, v in MOCK_USERS.items()]
