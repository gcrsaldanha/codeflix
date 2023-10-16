from rest_framework import serializers

from django.conf import settings

from core._shared.serializers.list_meta_response_serializer import ListMetaResponseSerializer
from core.cast_member.domain import CastMemberType


class EnumField(serializers.ChoiceField):
    # TODO: find a better way to serialize enums
    def __init__(self, enum, **kwargs):
        self.enum = enum
        kwargs['choices'] = [(e.name, e.value) for e in enum]
        super(EnumField, self).__init__(**kwargs)

    def to_representation(self, obj):
        if type(obj) == str:
            return obj
        else:
            return obj.name

    def to_internal_value(self, data):
        try:
            return self.enum[data]
        except KeyError:
            self.fail('invalid_choice', input=data)


class CastMemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    cast_member_type = EnumField(enum=CastMemberType)


class ListCastMembersRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=settings.DEFAULT_PAGE_SIZE)


class ListCastMembersResponseSerializer(serializers.Serializer):
    data = CastMemberSerializer(many=True)
    meta = ListMetaResponseSerializer()


class GetCastMemberRequestSerializer(serializers.Serializer):
    cast_member_id = serializers.UUIDField()


class GetCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberSerializer(source="cast_member")


class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    cast_member_type = EnumField(enum=CastMemberType)


class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberRequestSerializer(serializers.Serializer):
    cast_member_id = serializers.UUIDField()
    name = serializers.CharField(required=True)
    cast_member_type = EnumField(enum=CastMemberType)


class UpdateCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberSerializer(source="cast_member")


class PartialUpdateCastMemberRequestSerializer(serializers.Serializer):
    cast_member_id = serializers.UUIDField()
    name = serializers.CharField(required=False)
    cast_member_type = EnumField(enum=CastMemberType, required=False)


class PartialUpdateCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberSerializer(source="cast_member")


class DeleteCastMemberRequestSerializer(serializers.Serializer):
    cast_member_id = serializers.UUIDField()
