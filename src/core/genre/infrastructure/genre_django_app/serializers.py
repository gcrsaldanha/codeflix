from rest_framework import serializers

from django.conf import settings

from core._shared.serializers.list_meta_response_serializer import ListMetaResponseSerializer


class GenreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField(), default=[])


class ListGenresRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=settings.DEFAULT_PAGE_SIZE)


class ListGenresResponseSerializer(serializers.Serializer):
    data = GenreSerializer(many=True)
    meta = ListMetaResponseSerializer()


class GetGenreRequestSerializer(serializers.Serializer):
    genre_id = serializers.UUIDField()


class GetGenreResponseSerializer(serializers.Serializer):
    data = GenreSerializer(source="genre")


class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    categories = serializers.ListField(child=serializers.UUIDField(), required=False)


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreRequestSerializer(serializers.Serializer):
    genre_id = serializers.UUIDField()
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True, allow_null=False)
    is_active = serializers.BooleanField(required=True)


class UpdateGenreResponseSerializer(serializers.Serializer):
    pass


class PartialUpdateGenreRequestSerializer(serializers.Serializer):
    genre_id = serializers.UUIDField()
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)


class PartialUpdateGenreResponseSerializer(serializers.Serializer):
    pass


class DeleteGenreRequestSerializer(serializers.Serializer):
    genre_id = serializers.UUIDField()
