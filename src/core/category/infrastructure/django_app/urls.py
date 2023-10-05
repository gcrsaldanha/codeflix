from django.urls import path

from core.category.infrastructure.django_app.views import ListCategoryView

urlpatterns = [
    path("api/categories/", ListCategoryView.as_view(), name="list_categories"),
]
