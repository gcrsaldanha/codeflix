from uuid import UUID, uuid4

import pytest

from core._shared.notification.notification_error import NotificationException
from core.cast_member.domain.entity.cast_member import CastMemberType, CastMember


class TestCastMemberInit:
    def test_create_cast_member_with_auto_id(self):
        cast_member = CastMember(name="John Doe", cast_member_type=CastMemberType.ACTOR)
        assert cast_member.name == "John Doe"
        assert cast_member.cast_member_type == CastMemberType.ACTOR
        assert cast_member.id is not None
        assert isinstance(cast_member.id, UUID)

    def test_create_cast_member_with_given_id(self):
        given_category_id = uuid4()
        cast_member = CastMember(name="John Doe", cast_member_type=CastMemberType.ACTOR, id=given_category_id)
        assert cast_member.name == "John Doe"
        assert cast_member.cast_member_type == CastMemberType.ACTOR
        assert cast_member.id == given_category_id

    def test_when_name_is_empty_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="name cannot be empty"):
            CastMember(name="", cast_member_type=CastMemberType.ACTOR)

    def test_when_is_larger_than_255_characters_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="name cannot be longer than 255 characters"):
            CastMember(name="a" * 256, cast_member_type=CastMemberType.ACTOR)

    def test_when_cast_member_type_is_empty_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="type cannot be empty"):
            CastMember(name="John Doe", cast_member_type=None)

    def test_when_multiple_errors_then_raise_multiple_notification_error(self):
        expected_notification_message = "cast_member: name cannot be empty,cast_member: type cannot be empty"  # noqa: E501
        with pytest.raises(NotificationException, match=expected_notification_message):
            CastMember(name="", cast_member_type=None)


class TestChangeCastMember:
    def test_cahnge_cast_member_name_and_type(self):
        cast_member = CastMember(name="John Doe", cast_member_type=CastMemberType.ACTOR)
        cast_member.change_cast_member(name="Mary Stuart",  cast_member_type=CastMemberType.DIRECTOR)
        assert cast_member.name == "Mary Stuart"
        assert cast_member.cast_member_type == CastMemberType.DIRECTOR

    def test_when_name_is_empty_then_add_notification_error(self):
        cast_member = CastMember(name="John Doe", cast_member_type=CastMemberType.ACTOR)
        cast_member.change_cast_member(name="", cast_member_type=CastMemberType.DIRECTOR)
        assert cast_member.notification.has_errors()
        assert cast_member.notification.messages() == "cast_member: CastMember name cannot be empty"
