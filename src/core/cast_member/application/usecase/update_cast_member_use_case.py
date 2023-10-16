from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.cast_member.application.usecase.exceptions import UpdateCastMemberException, CastMemberDoesNotExist
from core.cast_member.domain import CastMemberType, CastMember
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository


@dataclass
class UpdateCastMemberInput:
    cast_member_id: UUID
    name: Optional[str] = None
    cast_member_type: Optional[CastMemberType] = None


@dataclass
class UpdateCastMemberOutput:
    cast_member: CastMember


class UpdateCastMemberUseCase(UseCase[UpdateCastMemberInput, UpdateCastMemberOutput]):
    def __init__(self, repository: Optional[CastMemberRepositoryInterface] = None):
        self._repository = repository or CastMemberDjangoRepository()

    def execute(self, request: UpdateCastMemberInput) -> UpdateCastMemberOutput:
        cast_member = self._repository.get_by_id(request.cast_member_id)
        if cast_member is None:
            raise CastMemberDoesNotExist(f"CastMember with id {request.cast_member_id} does not exist")

        # Only update fields that are provided
        if request.name is None:
            request.name = cast_member.name

        if request.cast_member_type is None:
            request.cast_member_type = cast_member.cast_member_type

        cast_member.change_cast_member(request.name, request.cast_member_type)
        if cast_member.notification.has_errors():
            raise UpdateCastMemberException(cast_member.notification.errors)

        self._repository.update(cast_member)

        return UpdateCastMemberOutput(cast_member)
