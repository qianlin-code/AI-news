"""
模型基类 — 所有 ORM 模型共用同一个 Base
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
