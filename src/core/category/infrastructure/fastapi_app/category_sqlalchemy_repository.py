from typing import Optional, Dict, Any, Sequence
from uuid import UUID

from sqlalchemy import desc, asc, and_
from sqlalchemy.orm import Session

from core._shared.listing.orderer import Order
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface


# TODO: when using Postgres, we don't need to convert UUID to str
class CategorySQLAlchemyRepository(CategoryRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create(self, category: Category) -> None:
        category.id = str(category.id)
        self.session.add(category)
        self.session.commit()

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return self.session.query(Category).filter_by(id=str(category_id)).first()

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = 50,  # TODO: Change this to settings.DEFAULT_PAGE_SIZE
        offset: int = 0,
    ) -> Sequence[Category]:
        filters = filters or {}
        order_by = order_by or {"name": Order.ASC}

        # Convert the order_by dict to a format suitable for SQLAlchemy.
        order_by_converted = []
        for field, order in order_by.items():
            column = getattr(Category, field, None)
            if column:
                if order == Order.DESC:
                    order_by_converted.append(desc(column))
                else:
                    order_by_converted.append(asc(column))

        query = self.session.query(Category).filter_by(**filters).order_by(*order_by_converted)

        # Applying offset and limit
        query = query.offset(offset).limit(limit)

        # Transform ORM entity instances back into domain entity instances
        result = [
            Category(
                id=UUID(orm_category.id),
                name=orm_category.name,
                description=orm_category.description,
                is_active=orm_category.is_active,
            )
            for orm_category in query
        ]

        return result

    def update(self, category: Category) -> None:
        category.id = str(category.id)
        self.session.merge(category)
        self.session.commit()

    def delete(self, category_id: UUID) -> None:
        category = self.session.query(Category).filter_by(id=str(category_id)).first()
        self.session.delete(category)
        self.session.commit()

    def count(self, filters: Optional[Dict] = None) -> int:
        filters = filters or {}
        query = self.session.query(Category).filter_by(**filters)
        return query.count()
