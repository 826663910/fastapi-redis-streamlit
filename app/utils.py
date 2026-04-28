# pip install pwdlib[argon2] 下载哈希加密的库
from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

# 哈希加密
def hash(password: str) -> str:
    return password_hash.hash(password)

# 验证密码
def verify(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)