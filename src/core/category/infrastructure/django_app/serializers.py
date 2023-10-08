from rest_framework import serializers


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


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
