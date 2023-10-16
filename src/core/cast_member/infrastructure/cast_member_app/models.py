from uuid import uuid4

from django.db import models

from core.cast_member.domain import CastMemberType


class CastMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    # TODO: optimization – make this an integer / indexable
    cast_member_type = models.CharField(max_length=255, choices=[(tag.name, tag.value) for tag in CastMemberType])
