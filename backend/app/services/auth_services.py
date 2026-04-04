from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Temporary in-memory DB (for prototype)
fake_db = {}

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def signup_user(username, password):
    if username in fake_db:
        return {"error": "User already exists"}

    hashed = hash_password(password)

    fake_db[username] = hashed

    return {"message": "User created successfully"}


def login_user(username, password):
    if username not in fake_db:
        return {"error": "User not found"}

    hashed = fake_db[username]

    if not verify_password(password, hashed):
        return {"error": "Invalid password"}

    return {"message": "Login successful"}