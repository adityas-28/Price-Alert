import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-for-jwt")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
SENDER_EMAIL = "pricealert95@gmail.com"
SENDER_PASS = "xpmefsqvqozcewdr"