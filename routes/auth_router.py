from aiosmtplib import SMTPResponseException
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import string
import random
from dependencies import get_mail, get_session
from repository.user_repo import EmailCodeRepository
from schemas import ResponseOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/code", response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query(...)],
        mail: FastMail = Depends(get_mail),
        session: AsyncSession = Depends(get_session)
):
    # 1. 生成验证码
    source = string.digits * 4
    code = "".join(random.sample(source, 4))
    # 2. 创建消息
    message = MessageSchema(subject="[ai-name]注册验证码", recipients=[email],
                            body=f"您的验证码为：{code}，有效期10分钟！", subtype=MessageType.plain)
    try:
        await mail.send_message(message)
        repo = EmailCodeRepository(session=session)
        await repo.create(email=str(email), code=code)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("忽略QQ邮箱SMTP关闭阶段的非标准响应（邮件已发送成功）")

        else:
            raise HTTPException(status_code=500, detail="邮件发送失败！")
    return ResponseOut()
