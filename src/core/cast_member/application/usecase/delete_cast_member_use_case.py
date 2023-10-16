from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.cast_member.application.usecase.exceptions import CastMemberDoesNotExist
from core.cast_member.domain import CastMember
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository


@dataclass
class DeleteCastMemberInput:
    cast_member_id: UUID


@dataclass
class DeleteCastMemberOutput:
    cast_member: CastMember


class DeleteCastMemberUseCase(UseCase[DeleteCastMemberInput, DeleteCastMemberOutput]):
    def __init__(self, repository: Optional[CastMemberRepositoryInterface] = None):
        self._repository = repository or CastMemberDjangoRepository()

    def execute(self, request: DeleteCastMemberInput) -> DeleteCastMemberOutput:
        cast_member = self._repository.get_by_id(request.cast_member_id)
        if cast_member is None:
            raise CastMemberDoesNotExist(f"CastMember with id {request.cast_member_id} does not exist")

        self._repository.delete(cast_member.id)

        return DeleteCastMemberOutput(cast_member)
