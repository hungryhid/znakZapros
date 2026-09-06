import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from os import getenv
import dotenv
import enum

dotenv.load_dotenv()
url = getenv("DATABASE_URL")



engine = create_async_engine(url=url, echo=True) #type: ignore

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session


base = declarative_base()

class Companyrole(enum.Enum):
    member = "member"
    coadmin = "co-admin"
    admin = "admin"
    owner = "owner"

class Statuscode(enum.Enum):
    wait = "wait"
    process = "process"
    complete = "complete"
    failed = "failed"



class User(base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(),nullable=False)

class Company(base):
    __tablename__ = "companies"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

class Companymember(base):
    __tablename__ = "company_members"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(Enum(Companyrole), nullable=False, default=Companyrole.member)


class Product(base):
    __tablename__ = "products"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)


class Code_request(base):
    __tablename__ = "code_requests"
    id = Column(Integer, nullable=False, primary_key=True)
    product_id = Column(Integer,ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    status = Column(Enum(Statuscode), nullable=False, default=Statuscode.wait)
    quantity = Column(Integer, CheckConstraint("quantity >= 1"), nullable=False)

class Code(base):
    __tablename__ = "codes"
    id = Column(Integer, nullable=False, primary_key=True)
    code_request_id = Column(Integer, ForeignKey("code_requests.id"), nullable=False)
    value = Column(String, nullable=False)


