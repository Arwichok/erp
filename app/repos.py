from pprint import pprint
from typing import Generic, Self

from litestar.plugins.sqlalchemy import repository
from sqlalchemy.ext.asyncio import AsyncSession

from .dto import WriteUserDTO
from .models import User


class Repository(repository.SQLAlchemyAsyncRepository, Generic[repository.ModelT]):
    @classmethod
    async def provide(cls, db_session: AsyncSession) -> Self:
        return cls(session=db_session)


class UserRepository(Repository[User]):
    model_type = User

    async def create_user(self, user: User | WriteUserDTO) -> User:
        existed_user = await self.get_one_or_none(User.email == user.email)
        if existed_user:
            raise ValueError(f"User with email {user.email} already exists")
        else:
            return await self.add(
                User(
                    name=user.name,
                    email=user.email,
                    password=user.password,
                    salt="",
                ),
                auto_commit=True,
            )
