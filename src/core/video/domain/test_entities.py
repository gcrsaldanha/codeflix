import unittest
from uuid import UUID, uuid4
from decimal import Decimal

import pytest

from core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia
from core.video.domain.entities import Video
from core._shared.notification.notification_error import NotificationError, NotificationException


class TestVideoEntity:
    def test_valid_video(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=True,
            published=True,
            rating=Rating.AGE_12,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
        )

        # Check if the validation passes without errors
        video.validate()
        assert video.notification.has_errors() is False

    def test_invalid_video(self):
        video = Video(
            title=10,  # type: ignore[assignment]
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=True,
            published=True,
            rating=Rating.AGE_12,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
        )

        assert video.notification.has_errors() is False
        video.validate()

        assert video.notification.has_errors() is True
        error = next(video.notification.errors)  # TODO: why type error here?
        assert error == NotificationError(message="Input should be a valid string", context="title")

    def test_optional_attributes(self):
        # Create a Video object with optional attributes
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=True,
            published=True,
            rating=Rating.AGE_12,
            categories={uuid4()},
            genres={uuid4()},
            cast_members={uuid4()},
            banner=ImageMedia(uuid4(), "checksum", "banner.jpg", "path/to/banner"),
            thumbnail=None,  # Testing None value for an optional attribute
            trailer=AudioVideoMedia(uuid4(), "checksum", "trailer.mp4", "raw_path", "encoded_path", "COMPLETED"),
        )

        video.validate()
        assert video.notification.has_errors() is False
