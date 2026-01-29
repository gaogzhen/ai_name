from pydantic import BaseModel, Field
from typing import Annotated, Literal,List
from .agent import NameSchema

class NameIn(BaseModel):
    surname: Annotated[str, Field(..., description="姓氏")]
    gender: Annotated[Literal["不限", "男", "女"], Field(..., description="性别")]
    length: Annotated[Literal["不限", "单字", "双字", "三字", "四字"], Field(..., description="")]
    other: Annotated[str|None, Field("", description="其他要求")]
    exclude: Annotated[List[str], Field([], description="排除的名字")]

class NameOut(BaseModel):
    names: List[NameSchema]