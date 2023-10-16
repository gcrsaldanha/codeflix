from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.cast_member.domain.entity.cast_member import CastMember, CastMemberType
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberRepositoryInterface, \
    CastMemberDjangoRepository


@dataclass
class CreateCastMemberInput:
    name: str
    cast_member_type: CastMemberType

    def validate(self):
        pass


@dataclass
class CreateCastMemberOutput:
    id: UUID


class CreateCastMemberUseCase(UseCase[CreateCastMemberInput, CreateCastMemberOutput]):
    def __init__(self, repository: Optional[CastMemberRepositoryInterface] = None):
        self._repository = repository or CastMemberDjangoRepository()

    def execute(self, request: CreateCastMemberInput) -> CreateCastMemberOutput:
        entity = CastMember(name=request.name, cast_member_type=request.cast_member_type)

        self._repository.create(entity)

        return CreateCastMemberOutput(id=entity.id)
