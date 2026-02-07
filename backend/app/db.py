from collections.abc import AsyncGenerator
import uuid
from fastapi import Depends
from sqlalchemy import Column,String,Text,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession,AsyncEngine ,create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,relationship
from datetime import datetime,timezone
from fastapi_users.db import SQLAlchemyUserDatabase,SQLAlchemyBaseUserTableUUID

DATABASE_URL = "sqlite+aiosqlite:///./testt.db"


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__="Posts"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
    title=Column(Text)
    descrpt=Column(Text)
    created_datetime = Column(DateTime,default=datetime.now(timezone.utc))
    
    user = relationship("User",back_populates="posts")


class User(SQLAlchemyBaseUserTableUUID,Base):

    posts= relationship("Post",back_populates="user")





engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session:AsyncSession=Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session,User)