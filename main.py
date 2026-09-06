import fastapi
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import base, engine, get_db, User
from contextlib import asynccontextmanager
import security
import auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.user import UserCreate, UserLogin
bearer = HTTPBearer()


@asynccontextmanager
async def lifespan(app):
    await startup()
    yield
    await shutdown()

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

async def shutdown():
    await engine.dispose()

app = fastapi.FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
async def home(db = Depends(get_db)):
    return FileResponse("frontend/index.html")

async def get_current_user(db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    payload = auth.decode_access_token(token=token)
    user = await db.execute(select(User).where(User.id == int(payload["sub"])))
    return user.scalar_one_or_none()


@app.post("/register") #решил все таки поменять чтобы правильнее было
async def register(user: UserCreate, db = Depends(get_db)):

    user1 = await db.execute(select(User).where(User.email == user.email))
    if user1.scalar_one_or_none() != None:
        return fastapi.HTTPException(409)
    else:
        hashed_password = security.hash_password(password=user.password)
        newuser = User(
            name=user.name,
            password_hash=hashed_password,
            email=user.email
        )
        db.add(newuser)
        await db.commit()
        await db.refresh(newuser)
        return newuser.name, newuser.email
@app.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    userGET = await db.execute(select(User).where(User.email == user.email))
    user1 = userGET.scalar_one_or_none()
    if user1 != None:
        PasswordBool = security.hash_verify(user.password, user1.password_hash)
        if PasswordBool == True:
            return {
                "access_token": auth.create_access_token(user1.id)
            }
        else: 
            return "wrong password"
    else:
        return fastapi.HTTPException(401)

@app.get("/profile")
async def profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return {
    "id": user.id,
    "name": user.name,
    "email": user.email,
    "created_at": user.created_at
}
