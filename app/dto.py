from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from .models import User


class WriteUserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"created_at", "updated_at", "id", "salt"})

class ReadUserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password", "salt"})

class PayloadUserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(include={"email", "password"})
