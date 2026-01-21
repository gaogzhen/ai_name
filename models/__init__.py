from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import DB_URI

engine = create_async_engine(
    DB_URI,
    # 输出所有执行SQL的日志
    echo=True,
    # 连接池大小
    pool_size=10,
    # 运行连接池最大的连接数
    max_overflow=20,
    # 获得连接超时时间
    pool_timeout=10,
    # 连接回收时间
    pool_recycle=3600,
    # 连接前是否预检查
    pool_pre_ping=True
)

AsyncSessionFactory = sessionmaker(
    # 引擎
    bind=engine,
    # 异步会话
    class_=AsyncSession,
    # 是否在执行查找前执行flush操作
    autoflush=True,
    # 是否在执行commit之后session过期
    expire_on_commit=False,
)

# 定义命名约束的Base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        # index索引
        "ix": 'ix_%(column_0_label)s',
        # unique索引
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # check检查约束
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # foreign key
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # primary key
        "pk": "pk_%(table_name)s",

    })

from . import user