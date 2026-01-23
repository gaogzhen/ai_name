from aiosmtplib import SMTPResponseException
from fastapi import APIRouter, Query, Depends, HTTPException, Body
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import string
import random

from core.auth import AuthHandler
from dependencies import get_mail, get_session
from models.user import User
from repository.user_repo import EmailCodeRepository, UserRepository
from schemas import ResponseOut
from schemas.user import RegisterIn, UserCreateSchema, LoginIN

router = APIRouter(prefix="/auth", tags=["auth"])

auth_handler = AuthHandler()

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

@router.post("/register", response_model=ResponseOut)
async def register(
        data: RegisterIn,
        session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session=session)
    # 1. 判断邮箱是否存在
    email_exist = await user_repo.email_exist(email=str(data.email))
    if email_exist:
        raise HTTPException(400, detail="该邮箱已存在")

    # 2. 校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match = await email_code_repo.check_email_code(email=str(data.email), code=str(data.code))
    if not email_code_match:
        raise HTTPException(400, detail="验证码错误！")
    # 3. 创建用户
    try:
        await user_repo.create(UserCreateSchema(email=data.email, username=data.username, password=data.password))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

    return ResponseOut()

@router.post("/login")
async def login(
        data: LoginIN,
        session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session=session)
    user: User = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(400, "邮箱不存在！")
    if not user.check_password(str(data.password)):
        raise HTTPException(400, "邮箱或者密码错误！")
    tokens = auth_handler.encode_login_token(user.id)
    user._password = ""
    return {
        "user": user,
        "token": tokens['access_token'],
    }