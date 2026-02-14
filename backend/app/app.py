from fastapi import FastAPI,HTTPException,File,UploadFile,Form,Depends
from typing import Optional
from app.schemas.schemas import CreatePost,UserCreate,UserRead,UserUpdate
from app.db import Post,create_db_and_tables,create_async_engine,get_async_session,User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import uuid
from sqlalchemy.orm import selectinload
from app.users import auth_backend ,current_active_users,fastapi_users
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags = ["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix="/auth",tags = ["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags = ["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags = ["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix="/users",tags = ["users"])

@app.post("/post")
async def post(post_data:CreatePost,user:User=Depends(current_active_users),session:AsyncSession=Depends(get_async_session)):
    post=Post(user_id=user.id,title=post_data.title,descrpt=post_data.description)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/showpost")
async def getposts(user:User=Depends(current_active_users),session:AsyncSession=Depends(get_async_session)):
    data = await session.execute(select(Post).options(selectinload(Post.user)).order_by(Post.created_datetime.desc()))
    posts=[row[0] for row in data.all()]
    post_data = []
    
    for post in posts:
        post_data.append({
            "user_id":str(user.id),
            "id":str(post.id),
            "title":post.title,
            "description":post.descrpt,
            "creation_time":post.created_datetime.isoformat(),
            "is_owner":str(post.user_id) == str(user.id)

        })
    return {"posts":post_data}


@app.delete("/deletepost/{post_id}")
async def deletepost(post_id:str,user:User=Depends(current_active_users),session:AsyncSession=Depends(get_async_session)):
    try:
        post_uuid=uuid.UUID(post_id)
        data = await session.execute(select(Post).where(Post.id == post_uuid))
        post = data.scalars().first()
        if not post:
            raise HTTPException(status_code=404,detail="Couldnt find post")
        
        if  post.user_id != user.id: # type: ignore[comparison-overlap]
            raise HTTPException(status_code=403,detail="Cant delete this post")
        
        await session.delete(post)
        await session.commit()

        return{"success":True,"message":"Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    


@app.put("/post/{post_id}")
async def update_post(post_id: str,post_data:CreatePost,user:User=Depends(current_active_users), session: AsyncSession = Depends(get_async_session)):
    post_uuid=uuid.UUID(post_id)
    result = await session.execute(select(Post).where(Post.id == post_uuid))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title=post_data.title # type: ignore
    post.descrpt=post_data.description   # type: ignore
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post 