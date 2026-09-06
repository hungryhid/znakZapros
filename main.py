import fastapi
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import base, engine, get_db, User
from contextlib import asynccontextmanager
import security
from schemas.user import UserCreate, UserLogin

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



@app.get("/")
async def home(db = Depends(get_db)):
    ex = select(User)
    users = await db.execute(ex)
    return users.scalars().all()


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
    itsUserOrNone = await db.execute(select(User).where(User.email == user.email))
    if itsUserOrNone.scalar_one_or_none() != None:
        user1 = itsUserOrNone.scalar_one()
        PasswordBool = security.hash_verify(user.password, user1.password_hash)
        if PasswordBool == True: return "ok"
        else: return "wrong password"
    else:
        return fastapi.HTTPException(401)

