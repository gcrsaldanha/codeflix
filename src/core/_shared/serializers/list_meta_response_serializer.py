from rest_framework import serializers


class ListMetaResponseSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    next_page = serializers.IntegerField(allow_null=True, default=None)
    total_quantity = serializers.IntegerField(default=0)
