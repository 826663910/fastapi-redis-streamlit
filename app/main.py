from fastapi import FastAPI
from contextlib import asynccontextmanager  # 异步上下文管理器
from fastapi.middleware.cors import CORSMiddleware  # cors中间件
from .databases import init_db, engine  # 初始化数据库, 获取session, 引擎
from .router import auth, posts, users



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

# 包含的路由器对象
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

