from typing import Optional
from uuid import UUID

from domain.category.entity.category import Category


class CategoryFactory:
    @staticmethod
    def create(name: str, description: str, is_active: bool = True, id: Optional[UUID] = None) -> Category:
        pass
