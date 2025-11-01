from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
import bcrypt
import hashlib
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def _prepare_password(password: str) -> bytes:
    """Prepare password for bcrypt: if > 72 bytes, pre-hash with SHA256."""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Pre-hash long passwords with SHA256 to get fixed 32-byte hash
        return hashlib.sha256(password_bytes).digest()
    return password_bytes

def hash_password(password: str) -> str:
    """Hash a password using bcrypt, handling passwords > 72 bytes."""
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prepared, salt)
    # Return as string for storage compatibility with passlib format
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    if not hashed_password:
        return False
    
    # Ensure hashed_password is a string and strip whitespace
    if not isinstance(hashed_password, str):
        hashed_password = str(hashed_password)
    hashed_password = hashed_password.strip()
    
    # Validate bcrypt hash format (should start with $2a$, $2b$, or $2y$)
    if not (hashed_password.startswith('$2a$') or hashed_password.startswith('$2b$') or hashed_password.startswith('$2y$')):
        return False
    
    prepared = _prepare_password(plain_password)
    
    # Convert string hash to bytes for bcrypt
    try:
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(prepared, hashed_bytes)
    except (ValueError, TypeError, AttributeError) as e:
        # Handle invalid hash format gracefully
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
