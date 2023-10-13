from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from core.category.application.usecase.create_category import CreateCategoryRequest, CreateCategory
from core.category.application.usecase.delete_category import DeleteCategoryRequest, DeleteCategory
from core.category.application.usecase.get_category import GetCategory, GetCategoryRequest
from core.category.application.usecase.list_categories import ListCategories, ListCategoriesRequest
from core.category.application.usecase.update_category import (
    UpdateCategoryRequest,
    UpdateCategory,
    CategoryDoesNotExist,
)
from core.category.infrastructure.django_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    GetCategoryRequestSerializer,
    GetCategoryResponseSerializer,
    ListCategoryResponseSerializer,
    PartialUpdateCategoryRequestSerializer,
    PartialUpdateCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
    UpdateCategoryResponseSerializer,
    ListCategoriesRequestSerializer,
)
from django.conf import settings


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        request_serializer = ListCategoriesRequestSerializer(
            data={
                "page": request.query_params.get("page", 1),
                "page_size": request.query_params.get("page_size", settings.DEFAULT_PAGE_SIZE),
            }
        )
        request_serializer.is_valid(raise_exception=True)
        use_case_request = ListCategoriesRequest(**request_serializer.validated_data)

        result = ListCategories().execute(use_case_request)
        response_serializer = ListCategoryResponseSerializer(result)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def retrieve(self, request, pk=None):
        request_serializer = GetCategoryRequestSerializer(data={"category_id": pk})
        request_serializer.is_valid(raise_exception=True)
        use_case_request = GetCategoryRequest(**request_serializer.validated_data)

        result = GetCategory().execute(use_case_request)
        if result.category is None:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": "Category not found"})

        response_serializer = GetCategoryResponseSerializer(result.category)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def create(self, request):
        request_serializer = CreateCategoryRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        use_case_request = CreateCategoryRequest(**request_serializer.validated_data)

        result = CreateCategory().execute(use_case_request)

        response_serializer = CreateCategoryResponseSerializer(result)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)

    def update(self, request, pk=None):  # TODO: activate / deactivate
        request_serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data.dict(),
                "category_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateCategoryRequest(**request_serializer.validated_data)
        try:
            result = UpdateCategory().execute(use_case_request)
        except CategoryDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = UpdateCategoryResponseSerializer(result.category)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def partial_update(self, request, pk=None):
        request_serializer = PartialUpdateCategoryRequestSerializer(
            data={
                **request.data.dict(),
                "category_id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)

        use_case_request = UpdateCategoryRequest(**request_serializer.validated_data)

        try:
            result = UpdateCategory().execute(use_case_request)
        except CategoryDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            response_serializer = PartialUpdateCategoryResponseSerializer(result.category)
            return Response(status=HTTP_200_OK, data=response_serializer.data)

    def destroy(self, request, pk=None):
        request_serializer = DeleteCategoryRequestSerializer(data={"category_id": pk})
        request_serializer.is_valid(raise_exception=True)

        use_case_request = DeleteCategoryRequest(**request_serializer.validated_data)

        try:
            DeleteCategory().execute(use_case_request)
        except CategoryDoesNotExist as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": str(error)})
        else:
            return Response(status=HTTP_204_NO_CONTENT)
