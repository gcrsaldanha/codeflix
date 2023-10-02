from domain.category.repository.category_repository_interface import CategoryRepositoryInterface


class UpdateCategory:
    def __init__(self, category_repository: CategoryRepositoryInterface = None):
        self.category_repository = category_repository

    def execute(self, category_id: int, category: Category):
        return self.category_repository.update(category_id, category)
