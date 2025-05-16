from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app import models, database, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi.security import APIKeyHeader

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "s3cr3t$super!long^key"

print("SECRET_KEY IN USE:", SECRET_KEY)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    print("ENCODING WITH SECRET:", SECRET_KEY)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user_by_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered.")

    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        message="User registered successfully",
    )

# LOGIN FIX
@router.post("/login", response_model=schemas.TokenResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db),
):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    access_token = create_access_token(data={"sub": db_user.email})

    from fastapi.responses import JSONResponse  # import here if not at top already

    return JSONResponse(content={    # <<< Fix: Force JSONResponse!
        "access_token": access_token,
        "token_type": "bearer"
    })

oauth2_scheme = APIKeyHeader(name="Authorization")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("DECODING WITH SECRET:", SECRET_KEY)
    print("Raw incoming token:", token)

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print("TOKEN PAYLOAD EMAIL:", email)
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    print("DB USER FOUND:", user)
    if user is None:
        raise credentials_exception
    
    return user 

@router.delete("/delete_user")
def delete_user(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
