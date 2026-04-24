from fastapi import FastAPI, HTTPException, Depends, status, Response
from contextlib import asynccontextmanager  # 异步上下文管理器
from fastapi.middleware.cors import CORSMiddleware  # cors中间件
from .databases import init_db, get_db, engine  # 初始化数据库, 获取session, 引擎
from sqlalchemy.ext.asyncio import AsyncSession # 异步session注解
from sqlalchemy import select   # 异步查询
from . import models, schemas    # 模型, 模式
from typing import List # 列表注解


# 在应用启动时, 调用init_db函数, 来执行create_all, 完成后自动关闭
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()
    

# 启动
app = FastAPI(lifespan=lifespan)


# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=List[schemas.PostOut])
async def posts(db: AsyncSession = Depends(get_db), limit: int = 10, skip: int = 0):
    # 查询所有文章
    stmt = select(models.Post).order_by(models.Post.id).limit(limit).offset(skip)
    result = await db.execute(stmt) # 查询需要异步
    posts = result.scalars().all()
    return posts


@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.Post, 
                      db: AsyncSession = Depends(get_db)):
    # 创建新文章
    new_post = models.Post(**post.model_dump())
    print(new_post)
    db.add(new_post)
    await db.commit()  # 提交需要异步
    await db.refresh(new_post)  # 刷新需要异步
    return new_post

@app.get('/{id}', response_model=schemas.PostOut)
async def post(id: int, db: AsyncSession = Depends(get_db)):
    # 查询单个文章
    stmt = select(models.Post).where(models.Post.id==id)
    result = await db.execute(stmt) # 查询需要异步
    post = result.scalar_one_or_none()  # 返回一个或者None

    # 如果为None, 抛出404异常
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    return post

@app.patch('/{id}')
async def update_post(id: int, post_data: schemas.PostUpdate, 
                     db: AsyncSession = Depends(get_db)):
    # 更新文章
    stmt = select(models.Post).where(models.Post.id==id)
    result = await db.execute(stmt) # 查询需要异步
    post = result.scalar_one_or_none()  # 返回一个或者None

    # 如果为None, 抛出404异常
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    # 动态更新属性字段
    for field, value in post_data.model_dump().items():
        setattr(post, field, value)
    
    await db.commit()  # 提交需要异步
    await db.refresh(post)  # 刷新需要异步
    return post

@app.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db)):
    # 删除文章
    stmt = select(models.Post).where(models.Post.id==id)
    result = await db.execute(stmt) # 查询需要异步
    post = result.scalar_one_or_none()  # 返回一个或者None

    # 如果为None, 抛出404异常
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    await db.delete(post)  # 删除需要异步
    await db.commit()  # 提交需要异步
    return Response(status_code=status.HTTP_204_NO_CONTENT)