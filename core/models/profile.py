from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import String, Text, ForeignKey
from .base import Base
from typing import Union
from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[Union[str, None]] = mapped_column(String(40), unique=False)
    last_name: Mapped[Union[str, None]] = mapped_column(String(40), unique=False)
    bio: Mapped[Union[str, None]]
