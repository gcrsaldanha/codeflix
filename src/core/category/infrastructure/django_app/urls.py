from django.urls import path

from core.category.infrastructure.django_app.views.get_category_view import GetCategoryView
from core.category.infrastructure.django_app.views.list_category_view import ListCategoryView

urlpatterns = [
    path("", ListCategoryView.as_view(), name="list_categories"),
    path("<str:category_id>/", GetCategoryView.as_view(), name="get_category"),
]
