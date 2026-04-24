from pydantic import BaseModel  # 基础验证库
from typing import Optional # 类型注解
from datetime import datetime

# 请求头
class Post(BaseModel):
    title: str
    content: str
    publish: Optional[bool] = True  # 默认为True

# 更新
class PostUpdate(Post):
    pass

# 响应
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    publish: bool
    create_at: datetime
