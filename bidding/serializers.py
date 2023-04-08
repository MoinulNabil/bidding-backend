from rest_framework import serializers

from .models import (
    Product,
    PlacedBid
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "title",
            "slug",
            "thumbnail",
            "price",
            "start_time",
            "ending_time",
            "description",
            "created_at",
        )


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "title",
            "slug",
            "thumbnail",
            "price",
            "start_time",
            "ending_time",
            "description",
            "created_at",
        )

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['user'] = {"email": instance.user.email, "phone": instance.user.phone}
        return context


class PlaceBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacedBid
        fields = (
            "id",
            "product",
            "user",
            "amount",
            "bid_time",
            "own",
        )

    def validate_amount(self, value):
         product = Product.objects.get(pk=self.get_initial().get('product'))
         less_amount = product.price > value
         bid = self.Meta.model.objects.filter(
             product=product,
             amount__gte=value
         )
         if less_amount:
             raise serializers.ValidationError(f"The minimum price is {product.price}")
         
         if bid.exists():
            raise serializers.ValidationError(f"You have to pay more than {value} to place a bid")
         
         return value
    

class UserBidSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(read_only=True)

    class Meta:
        model = PlacedBid
        fields = (
            "id",
            "product",
            "user",
            "amount",
            "bid_time",
            "own",
        )
