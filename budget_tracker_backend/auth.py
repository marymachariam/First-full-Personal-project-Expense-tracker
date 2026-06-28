# 1. Hash passwords
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

# 2. Create JWT token on login
from jose import jwt
def create_token(user_id: int):
    return jwt.encode({"sub": str(user_id)}, SECRET_KEY, algorithm="HS256")

# 3. Middleware to protect routes
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return db.query(User).filter(User.id == payload["sub"]).first()