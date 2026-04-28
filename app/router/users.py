from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession # 异步session注解
from sqlalchemy import select   # 查询
from .. import schemas, models, utils, oauth2   # 模式, 模型, 工具, 认证
from ..databases import get_db  # 操作数据库

# 实例化路由器
router = APIRouter(
    prefix="/users",    # 路径前缀
    tags=["users"],     # 标签   
)

# 注册用户
@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # 对密码进行哈希处理
    user.password = utils.hash(user.password)
    # 异常捕获
    try:
        # 创建新用户
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        await db.commit()  # 提交需要异步
        await db.refresh(new_user)  # 刷新需要异步
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT,   # 返回异常的http信息
                            detail=f"User already exists") 
    return new_user

# 获取用户
@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    # 查询用户
    stmt = select(models.User).where(models.User.id==id)
    # 执行sql
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # 返回一个或者None
    # 如果为None, 抛出404异常
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
