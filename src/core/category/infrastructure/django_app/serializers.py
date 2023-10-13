from rest_framework import serializers

from django.conf import settings


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoriesRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=settings.DEFAULT_PAGE_SIZE)


class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    next_page = serializers.IntegerField(allow_null=True, default=None)
    total_quantity = serializers.IntegerField(default=0)


class GetCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()


class GetCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True, allow_null=False)


class UpdateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class PartialUpdateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    category_id = serializers.UUIDField()


class PartialUpdateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class DeleteCategoryRequestSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
