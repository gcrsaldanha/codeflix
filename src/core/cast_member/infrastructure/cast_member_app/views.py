from django.conf import settings
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from core.cast_member.application.usecase.create_cast_member_use_case import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from core.cast_member.application.usecase.delete_cast_member_use_case import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)
from core.cast_member.application.usecase.exceptions import CastMemberDoesNotExist
from core.cast_member.application.usecase.get_cast_member_use_case import GetCastMemberUseCase, GetCastMemberInput
from core.cast_member.application.usecase.list_cast_members_use_case import ListCastMembersInput, ListCastMembersUseCase
from core.cast_member.application.usecase.update_cast_member_use_case import (
    UpdateCastMemberInput,
    UpdateCastMemberUseCase,
)
from core.cast_member.infrastructure.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    GetCastMemberRequestSerializer,
    GetCastMemberResponseSerializer,
    ListCastMembersResponseSerializer,
    PartialUpdateCastMemberRequestSerializer,
    PartialUpdateCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
    UpdateCastMemberResponseSerializer,
    ListCastMembersRequestSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        request_serializer = ListCastMembersRequestSerializer(
            data={
                "page": request.query_params.get("page", 1),
                "page_size": request.query_params.get("page_size", settings.DEFAULT_PAGE_SIZE),
            }
        )
        request_serializer.is_valid(raise_exception=True)
        use_case_request = ListCastMembersInput(**request_serializer.validated_data)

        result = ListCastMembersUseCase().execute(use_case_request)
        response_serializer = ListCastMembersResponseSerializer(result)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def retrieve(self, request, pk=None):
        request_serializer = GetCastMemberRequestSerializer(data={"cast_member_id": pk})
        request_serializer.is_valid(raise_exception=True)
        use_case_request = GetCastMemberInput(**request_serializer.validated_data)

        result = GetCastMemberUseCase().execute(use_case_request)
        if result.cast_member is None:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": "CastMember not found"})

        response_serializer = GetCastMemberResponseSerializer(result)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def create(self, request):
        request_serializer = CreateCastMemberRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        use_case_request = CreateCastMemberInput(**request_serializer.validated_data)

        result = CreateCastMemberUseCase().execute(use_case_request)

        response_serializer = CreateCastMemberResponseSerializer(result)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)

    def update(self, request, pk=None):
        request_serializer = UpdateCastMemberRequestSerializer(
            data={
                **request.data.dict(),
                "cast_member_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateCastMemberInput(**request_serializer.validated_data)
        try:
            result = UpdateCastMemberUseCase().execute(use_case_request)
        except CastMemberDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = UpdateCastMemberResponseSerializer(result)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def partial_update(self, request, pk=None):
        request_serializer = PartialUpdateCastMemberRequestSerializer(
            data={
                **request.data.dict(),
                "cast_member_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateCastMemberInput(**request_serializer.validated_data)

        try:
            result = UpdateCastMemberUseCase().execute(use_case_request)
        except CastMemberDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = PartialUpdateCastMemberResponseSerializer(result)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def destroy(self, request, pk=None):
        request_serializer = DeleteCastMemberRequestSerializer(data={"cast_member_id": pk})
        request_serializer.is_valid(raise_exception=True)

        use_case_request = DeleteCastMemberInput(**request_serializer.validated_data)

        try:
            DeleteCastMemberUseCase().execute(use_case_request)
        except CastMemberDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            return Response(status=HTTP_204_NO_CONTENT)
