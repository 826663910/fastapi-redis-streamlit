from fastapi import Depends, HTTPException, status, APIRouter   # 依赖, 异常, 状态码, 路由
from fastapi.security import OAuth2PasswordRequestForm  # 用户认证表单
from sqlalchemy.ext.asyncio import AsyncSession # 异步session注解
from sqlalchemy import select   # 异步查询
from ..databases import get_db # 操作数据库
from .. import models, utils, oauth2, schemas # 模型, 工具

# 路由器
router = APIRouter(
    tags=['Authentication']   # 标签
)

# 用户登录, 认证
@router.post('/login', response_model=schemas.Token)
async def user_login(userr_credentials: OAuth2PasswordRequestForm=Depends(),
                     db: AsyncSession = Depends(get_db)):
    # 查找用户
    stmt = select(models.User).where(models.User.email==userr_credentials.username)
    # 执行sql
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # 返回一个或者None
    # 如果为None, 抛出404异常
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    # 验证密码
    if not utils.verify(userr_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
    # 调用创建访问token的函数生成token
    token = oauth2.create_access_token(data={"user_id": user.id})
    # 返回token
    return {"access_token": token, "token_type": "bearer"}