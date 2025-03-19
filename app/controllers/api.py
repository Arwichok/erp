from http import HTTPStatus
from pprint import pprint

from litestar import Controller, Litestar, get, post, Request
from litestar.datastructures.state import State
from litestar.di import Provide
from litestar.exceptions import HTTPException

from ..dto import ReadUserDTO, WriteUserDTO, PayloadUserDTO
from ..models import User
from ..repos import UserRepository


class APIController(Controller):

    dto = WriteUserDTO
    return_dto = ReadUserDTO
    dependencies = {"user_repository": Provide(UserRepository.provide)}


    @get("/users")
    async def index(self, user_repository: UserRepository, request: Request) -> list[User]:
        pprint(request.app.state.get("engine"))

        return await user_repository.list()

    @post("/signup")
    async def register(self, data: User, user_repository: UserRepository, request: Request) -> User:
        # store = request.app.stores.get("memory")

        try:
            user = await user_repository.create_user(data)
            # await store.set(user.email, user.id)
            request.set_session({"user_id": user.id})
            return user
        except ValueError as e:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
        

    @post("/login", dto=PayloadUserDTO)
    async def login(self, data: User, user_repository: UserRepository, request: Request) -> User:
        store = request.app.stores.get("memory")

        user = await user_repository.get_one_or_none(User.email == data.email)
        if not user or user.password != data.password:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")
        
        await store.set(user.email, user.id)
        request.set_session({"user_id": user.id})
        return user


    @get("/user")
    async def get_user(self, user_repository: UserRepository, request: Request) -> User:
        # store = request.app.stores.get("memory")
        return await user_repository.get_one_or_none(User.id == request.session.get("user_id"))
    
