from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_router import router as auth_router
from routes.name_router import router as name_router
app = FastAPI()


# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"]    # 允许所有请求头
)

app.include_router(auth_router)
app.include_router(name_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

