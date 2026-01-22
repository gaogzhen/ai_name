from fastapi import FastAPI, Depends
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException

from dependencies import get_mail
from routes.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

