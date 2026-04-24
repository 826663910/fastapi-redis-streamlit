from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, BigInteger, Text, func
from sqlalchemy.sql.sqltypes import TIMESTAMP   # 导入数据库类型中的日期时间
from .databases import Base # 模型基类

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    publish = Column(Boolean, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
