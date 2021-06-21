from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Review, Order, Collection
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name'
                  )


class ProductSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductPosition(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    positions = ProductPosition(many=True)
    creator = serializers.CharField(source=UserSerializer, read_only=True)

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
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        user_objects = Review.objects.filter(creator=self.context["request"].user,
                                             review=validated_data["review"]).count()
        if self.context['request'].method == 'POST' and user_objects >= 1:
            raise ValidationError('Мы уже получили ваш отзыв. Спасибо!')
        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'
