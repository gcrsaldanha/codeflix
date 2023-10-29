"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.cast_member.infrastructure.cast_member_app.views import CastMemberViewSet
from core.category.infrastructure.django_app.views import CategoryViewSet
from core.genre.infrastructure.genre_django_app.views import GenreViewSet

router = DefaultRouter()
router.register(r"api/categories", CategoryViewSet, basename="category")
router.register(r"api/cast_members", CastMemberViewSet, basename="cast_member")
router.register(r"api/genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
