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

from core.genre.application.usecase.create_genre_use_case import CreateGenreInput, CreateGenreUseCase
from core.genre.application.usecase.delete_genre_use_case import DeleteGenreInput, DeleteGenreUseCase
from core.genre.application.usecase.get_genre_use_case import GetGenreUseCase, GetGenreInput
from core.genre.application.usecase.list_genres_use_case import ListGenresUseCase, ListGenresInput
from core.genre.application.usecase.update_genre_use_case import UpdateGenreInput, UpdateGenreUseCase
from core.genre.application.usecase.exceptions import GenreDoesNotExist
from core.genre.infrastructure.genre_django_app.serializers import (
    CreateGenreRequestSerializer,
    CreateGenreResponseSerializer,
    DeleteGenreRequestSerializer,
    GetGenreRequestSerializer,
    GetGenreResponseSerializer,
    ListGenresRequestSerializer,
    ListGenresResponseSerializer,
    PartialUpdateGenreRequestSerializer,
    PartialUpdateGenreResponseSerializer,
    UpdateGenreRequestSerializer,
    UpdateGenreResponseSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        request_serializer = ListGenresRequestSerializer(
            data={
                "page": request.query_params.get("page", 1),
                "page_size": request.query_params.get("page_size", settings.DEFAULT_PAGE_SIZE),
            }
        )
        request_serializer.is_valid(raise_exception=True)
        use_case_request = ListGenresInput(**request_serializer.validated_data)

        result = ListGenres().execute(use_case_request)
        response_serializer = ListGenresResponseSerializer(result)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def retrieve(self, request, pk=None):
        request_serializer = GetGenreRequestSerializer(data={"genre_id": pk})
        request_serializer.is_valid(raise_exception=True)
        use_case_request = GetGenreRequest(**request_serializer.validated_data)

        result = GetGenre().execute(use_case_request)
        if result.genre is None:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": "Genre not found"})

        response_serializer = GetGenreResponseSerializer(result)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def create(self, request):
        request_serializer = CreateGenreRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        use_case_request = CreateGenreRequest(**request_serializer.validated_data)

        result = CreateGenre().execute(use_case_request)

        response_serializer = CreateGenreResponseSerializer(result)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)

    def update(self, request, pk=None):
        request_serializer = UpdateGenreRequestSerializer(
            data={
                **request.data.dict(),
                "genre_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateGenreRequest(**request_serializer.validated_data)
        try:
            result = UpdateGenre().execute(use_case_request)
        except GenreDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = UpdateGenreResponseSerializer(result)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def partial_update(self, request, pk=None):
        request_serializer = PartialUpdateGenreRequestSerializer(
            data={
                **request.data.dict(),
                "genre_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateGenreRequest(**request_serializer.validated_data)

        try:
            result = UpdateGenre().execute(use_case_request)
        except GenreDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = PartialUpdateGenreResponseSerializer(result)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def destroy(self, request, pk=None):
        request_serializer = DeleteGenreRequestSerializer(data={"genre_id": pk})
        request_serializer.is_valid(raise_exception=True)

        use_case_request = DeleteGenreRequest(**request_serializer.validated_data)

        try:
            DeleteGenre().execute(use_case_request)
        except GenreDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            return Response(status=HTTP_204_NO_CONTENT)
