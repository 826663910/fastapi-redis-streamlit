from pydantic import BaseModel, EmailStr  # 基础验证库, 邮箱验证库
from typing import Optional, List # 类型注解
from datetime import datetime

"""用户"""
# 请求体
class User(BaseModel):
    email: EmailStr
    password: str

# 创建
class UserCreate(User):
    pass

# 响应
class UserOut(BaseModel):
    id: int
    email: str
    create_at: datetime

"""帖子"""
# 请求体
class Post(BaseModel):
    title: str
    content: str
    publish: Optional[bool] = True  # 默认为True
    

# 更新
class PostUpdate(Post):
    pass

# 响应
class PostOut(Post):
    id: int
    user_id: int
    owner: UserOut
    create_at: datetime



"""token认证"""
# 响应
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int