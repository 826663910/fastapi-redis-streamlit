from sqlalchemy import Column, String, Integer, Boolean, ForeignKey,Text, func
from sqlalchemy.sql.sqltypes import TIMESTAMP   # 导入数据库类型中的日期时间
from sqlalchemy.orm import relationship   # 导入关系映射
from .databases import Base # 模型基类

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    publish = Column(Boolean, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
