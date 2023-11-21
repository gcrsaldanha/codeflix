from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.cast_member.domain.entity.cast_member import CastMemberType


class CastMemberInterface(ABC):
    @abstractmethod
    def change_cast_member(self, name: str, cast_member_type: "CastMemberType") -> None:
        pass
