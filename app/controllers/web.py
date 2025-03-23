from pprint import pprint
from litestar import Controller, get, post, Request
from litestar.response import Template
from litestar.di import Provide
from ..dto import WriteUserDTO, ReadUserDTO, PayloadUserDTO
from ..models import User
from ..repos import UserRepository
from litestar.enums import RequestEncodingType
from litestar.params import Body
from typing import Annotated, TypeVar

T = TypeVar("T")
URLEncoded = Annotated[T, Body(media_type=RequestEncodingType.URL_ENCODED)]



class WebController(Controller):
    path = "/"
    dto = WriteUserDTO
    return_dto = ReadUserDTO
    dependencies = {"user_repository": Provide(UserRepository.provide)}

    @get("/")
    async def index(self, request: Request) -> Template:
        return Template("index.html.j2" , context={"request": request})
    

    @post("/signup")
    async def signup(self, data: URLEncoded[User], user_repository: UserRepository, request: Request) -> User:
        return await user_repository.create_user(data)

    @post("/login", dto=PayloadUserDTO)
    async def login(self, data: URLEncoded[User], user_repository: UserRepository, request: Request) -> User:
        store = request.app.stores.get("memory")
        print(f"{data.email} {data.password}")
        user = await user_repository.accept_user(data)
        pprint(user)
        await store.set(user.email, user.id)
        request.set_session({"user_id": user.id})
        return user

    