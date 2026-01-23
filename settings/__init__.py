import os
from datetime import timedelta

# 数据库相关配置
DB_URI = "mysql+aiomysql://root:mysql8#Fastapi@localhost:3306/ai_name?charset=utf8mb4"
# 邮箱相关配置
MAIL_USERNAME = "806797785@qq.com"
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_FROM = "806797785@qq.com"
MAIN_FROM_NAME = "gaogzhen"
MAIN_STARTTLS = True
MAIL_SSL_TLS = False

# 权限相关配置
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
