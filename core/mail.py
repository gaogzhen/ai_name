from fastapi_mail import FastMail, ConnectionConfig
from pydantic import SecretStr, EmailStr
import settings


def create_mail_instance() -> FastMail:
    """创建 FastMail 实例（每次调用返回新实例，线程/协程安全）"""
    main_config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=SecretStr(settings.MAIL_PASSWORD),
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_FROM_NAME=settings.MAIN_FROM_NAME,
        MAIL_STARTTLS=settings.MAIN_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )
    return FastMail(main_config)

