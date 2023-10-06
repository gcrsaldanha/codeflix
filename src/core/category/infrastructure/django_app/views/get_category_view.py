from uuid import UUID

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from core.category.application.usecase.category.get_category import GetCategory, GetCategoryRequest


class GetCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()

class GetCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class GetCategoryView(APIView):
    def get(self, request, category_id: str):
        request_serializer = GetCategoryRequestSerializer(data={"category_id": category_id})
        request_serializer.is_valid(raise_exception=True)

        result = GetCategory().execute(GetCategoryRequest(category_id=request_serializer.validated_data["category_id"]))
        if result.category is None:
            return Response(status=404, data={"message": "Category not found"})

        serializer = GetCategoryResponseSerializer(result.category)

        return Response(serializer.data)
