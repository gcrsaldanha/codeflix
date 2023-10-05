from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from core.category.application.usecase.category.list_categories import ListCategories, ListCategoriesRequest


class ListCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryView(APIView):
    def get(self, request):
        categories = ListCategories().execute(ListCategoriesRequest())

        serializer = ListCategorySerializer(categories, many=True)

        return Response(serializer.data)
