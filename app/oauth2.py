# pip install pyjwt 下载jwt的库
import jwt  # jwt库
from jwt.exceptions import InvalidTokenError    # jwt异常处理
from datetime import datetime, timedelta, timezone  # 时间库
from fastapi import Depends, HTTPException, status  # 依赖注入, 异常处理, 响应码
from fastapi.security import OAuth2PasswordBearer   # 获取访问token的依赖关系
from sqlalchemy.ext.asyncio import AsyncSession # 异步session注解
from sqlalchemy import select   # 查询
from . import schemas, models   # 模式, 模型
from .databases import get_db # 操作数据库

# 定义令牌提取器，获取登录接口的令牌(自动获取)
oath_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 创建访问token, 声明是字典格式
def create_access_token(data: dict):
    to_encode = data.copy()  # 拷贝一份, 不改变原始数据
    # 令牌到期时间
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 对数据副本提供过期时间
    to_encode.update({"exp": expire})
    # 使用密钥和算法对数据进行编码
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 返回编码后的令牌
    return encoded_jwt

# 验证访问的token, (token标记, 凭证异常)
def verify_access_token(token: str, credentials_exception):
    # 异常捕获
    try:
        # 使用密钥和算法对数据进行解码
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 返回解码后的数据
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # 如果有id赋值给TokenData, 做类型验证
        token_data = schemas.TokenData(user_id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data


# 作为路径操作的依赖关系(主要是获取验证凭证后获取用户信息给到其他路径, 和传递凭证异常信息)
async def get_current_user(token: str = Depends(oath_scheme),
                     db: AsyncSession = Depends(get_db)):
    # 传递凭证异常信息
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # 调用验证访问令牌(返回当前登录的用户id)
    token = verify_access_token(token, credentials_exception)
    # 查询用户信息
    stmt = select(models.User).where(models.User.id==token.user_id)
    result = await db.execute(stmt)  # 异步执行查询
    user = result.scalar_one_or_none()  # 返回一个或者None
    # 如果为None, 抛出404异常
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
