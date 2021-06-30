from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, ProductReview, Order, Collection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.Serializer):

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product.id"
    )

    name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True, min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    creator = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, ()
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ()
        return self.instance

    def validate(self, data):
        positions = getattr('positions')
        if not positions:
            raise ValidationError({'products': 'Ваша корзина пуста'})


class ReviewSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        data["creator"] = self.context["request"].user
        user_objects = ProductReview.objects.filter(creator=self.context["request"].user,
                                                    review_product=data["review_product"]).count()
        if self.context['request'].method == 'POST' and user_objects >= 1:
            raise ValidationError('Мы уже получили ваш отзыв. Спасибо!')


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'
