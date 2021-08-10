from rest_framework import serializers
from . import models
import csv


class ProductSerializer(serializers.ModelSerializer):
    """
        Serializer class form inventory.product
    """

    class Meta:
        model = models.Product
        fields = (
            'name',
            'description',
            'price',
        )


class FruitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=False, allow_blank=False, required=True, max_length=50)

    def create(self, validated_data):
        with open('/tmp/fruit-report.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(validated_data['name'])
        return validated_data

    def update(self, instance, validated_data):
        pass
