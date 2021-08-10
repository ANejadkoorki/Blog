from rest_framework import serializers
from . import models


class OrderSeralizer(serializers.ModelSerializer):
    """
        Serializer for Store.Order
    """

    class Meta:
        model = models.Order
        fields = (
            'pk',  # TODO make sure pk is readonly
            'owner',
            'status',
        )
