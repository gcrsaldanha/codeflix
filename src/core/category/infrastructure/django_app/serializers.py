from rest_framework import serializers

from django.conf import settings

from core._shared.serializers.list_meta_response_serializer import ListMetaResponseSerializer


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoriesRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=settings.DEFAULT_PAGE_SIZE)


class ListCategoriesResponseSerializer(serializers.Serializer):
    data = CategorySerializer(many=True)
    meta = ListMetaResponseSerializer()


class GetCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()


class GetCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="category")


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True, allow_null=False)
    is_active = serializers.BooleanField(required=True)


class UpdateCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="category")


class PartialUpdateCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)


class PartialUpdateCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="category")


class DeleteCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
