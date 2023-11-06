from uuid import uuid4

from sqlalchemy import MetaData, Table, Column, String, Boolean, Uuid  # DO NOT USE UUID!
from sqlalchemy.orm import registry

from core.category.domain import Category

metadata = MetaData()

categories = Table(
    "categories",
    metadata,
    Column("id", String, primary_key=True, default=uuid4),  # TODO: make Uuid
    Column("name", String, nullable=False),
    Column("description", String, default=""),
    Column("is_active", Boolean, default=True),
)


def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(Category, categories)
