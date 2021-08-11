from rest_framework import serializers

from users.serializers import UserSerializer
from . import models


class OrderSeralizer(serializers.HyperlinkedModelSerializer):
    """
        Serializer for Store.Order
    """
    # orderitem_set = serializers.HyperlinkedRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = (
            'pk',  # TODO make sure pk is readonly
            'owner',
            'status',
            'orderitem_set',
        )


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer for Store.OrderItem
    """

    class Meta:
        model = models.OrderItem
        fields = (
            'id',
            'product',
            'qty',
            'discount',
            'price',

        )
