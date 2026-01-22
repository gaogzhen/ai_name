import os

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

