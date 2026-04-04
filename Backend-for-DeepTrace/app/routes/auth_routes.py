from fastapi import APIRouter
from app.models.user_models import UserSignup, UserLogin
from app.services.auth_services import signup_user, login_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    return signup_user(user.username, user.password)


@router.post("/login")
def login(user: UserLogin):
    return login_user(user.username, user.password)