from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase



class User(base.UUIDAuditBase):
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    salt: Mapped[bytes] = mapped_column(nullable=False)



metadata = base.UUIDAuditBase.metadata
