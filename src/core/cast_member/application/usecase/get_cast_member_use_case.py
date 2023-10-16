from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.cast_member.domain import CastMember
from core.cast_member.infrastructure.cast_member_app.repositories import (
    CastMemberRepositoryInterface,
    CastMemberDjangoRepository,
)


@dataclass
class GetCastMemberInput:
    cast_member_id: UUID


@dataclass
class GetCastMemberOutput:
    cast_member: Optional[CastMember]


class GetCastMemberUseCase(UseCase[GetCastMemberInput, GetCastMemberOutput]):
    def __init__(self, repository: Optional[CastMemberRepositoryInterface] = None):
        self._repository = repository or CastMemberDjangoRepository()

    def execute(self, request: GetCastMemberInput) -> GetCastMemberOutput:
        cast_member = self._repository.get_by_id(request.cast_member_id)
        return GetCastMemberOutput(cast_member)
