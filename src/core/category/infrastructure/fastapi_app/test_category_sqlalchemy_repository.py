import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from core.category.domain import Category
from core.category.infrastructure.fastapi_app.category_sqlalchemy_repository import CategorySQLAlchemyRepository
from core.category.infrastructure.fastapi_app.orm import start_mappers, metadata


# Tests below were generated by ChatGPT for simplicity
@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    SessionMaker = sessionmaker(bind=in_memory_db)
    return SessionMaker()


@pytest.fixture
def category_repo(session):
    start_mappers()
    yield CategorySQLAlchemyRepository(session)
    clear_mappers()


def test_can_add_and_retrieve_category(category_repo):
    category = Category(name="Electronics")
    category_repo.create(category)

    retrieved = category_repo.get_by_id(category.id)
    assert retrieved == category


def test_can_add_and_retrieve_multiple_categories(category_repo):
    category1 = Category(name="Electronics")
    category2 = Category(name="Books")
    category_repo.create(category1)
    category_repo.create(category2)

    assert len(category_repo.get_all()) == 2


def test_can_update_category(category_repo):
    category = Category(name="Electronics")
    category_repo.create(category)

    category.name = "Gadgets"
    category_repo.update(category)

    retrieved = category_repo.get_by_id(category.id)
    assert retrieved.name == "Gadgets"


def test_can_delete_category(category_repo):
    category = Category(name="Electronics")
    category_repo.create(category)

    category_repo.delete(category.id)

    assert category_repo.get_by_id(category.id) is None


def test_can_count_categories(category_repo):
    category1 = Category(name="Electronics")
    category2 = Category(name="Books")
    category_repo.create(category1)
    category_repo.create(category2)

    count = category_repo.count()
    assert count == 2


def test_get_all_paginating(category_repo):
    category1 = Category(name="Electronics")
    category2 = Category(name="Books")
    category3 = Category(name="Clothes")
    category_repo.create(category1)
    category_repo.create(category2)
    category_repo.create(category3)

    retrieved = category_repo.get_all(limit=2, offset=1)
    assert len(retrieved) == 2
    assert retrieved[0].name == "Clothes"  # Skipped "Books"
    assert retrieved[1].name == "Electronics"
