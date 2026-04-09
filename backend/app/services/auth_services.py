from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.database import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def normalize_username(username):
    return username.strip().lower()


def signup_user(username, password):
    normalized_username = normalize_username(username)

    if not normalized_username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )

    existing_user = users_collection.find_one({"username": normalized_username})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    hashed = hash_password(password)

    users_collection.insert_one(
        {
            "username": normalized_username,
            "password": hashed,
        }
    )

    return {"message": "User created successfully", "username": normalized_username}


def login_user(username, password):
    normalized_username = normalize_username(username)

    user = users_collection.find_one({"username": normalized_username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    hashed = user["password"]

    if not verify_password(password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    return {"message": "Login successful", "username": normalized_username}