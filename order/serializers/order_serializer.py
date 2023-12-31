from rest_framework import serializers

from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    products_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total
    
    class Meta:
        model = Order
        fields = ['product', 'products_id', 'user','total']
        extra_kwargs = {'product': {'required: False'}}

    def create(self, validated_data):
        product_data = validated_data.pop('products_id')
        user_data = validated_data.pop('user')

        order = Order.objects.create(validated_data)
        for product in product_data:
            order.product.add(product)
        
        for user in user_data:
            order.product.add(user)

        return order