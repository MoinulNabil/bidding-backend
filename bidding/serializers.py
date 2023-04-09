from django.db.models import Max

from rest_framework import serializers

from .models import (
    Product,
    PlacedBid
)


def update_placed_bid_status(instance):
        bids = PlacedBid.objects.filter(product=instance)
        if bids.exists() and not instance.available:
            winning_bid = bids.order_by('-amount').first()
            winning_bid.own = True
            winning_bid.save()
            instance.active = False
            instance.save()


class PlaceBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacedBid
        fields = (
            "id",
            "product",
            "user",
            "amount",
            "bid_time",
        )

    def validate_amount(self, value):
         product = Product.objects.get(pk=self.get_initial().get('product'))
         less_amount = product.price > value
         bid = self.Meta.model.objects.filter(
             product=product,
             amount__gte=value
         )
         if less_amount:
             raise serializers.ValidationError(f"The product base price is {product.price}")
         
         if bid.exists():
            raise serializers.ValidationError(f"The minimum bidding price must be greater than {bid.first().amount}")
         
         return value
    
    def validate(self, validated_data):
         product = Product.objects.get(pk=validated_data.get('product').id)
         if not product.available:
            raise serializers.ValidationError("The bid is not active")
         return validated_data
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['user'] = {'email': instance.user.email, 'phone': instance.user.phone}
        return context



class ProductSerializer(serializers.ModelSerializer):
    total_bids = serializers.SerializerMethodField(method_name='get_total_bids')

    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "title",
            "slug",
            "thumbnail",
            "price",
            "ending_time",
            "description",
            "total_bids",
            "created_at",
        )

    def get_total_bids(self, obj):
        return PlacedBid.objects.filter(product=obj).count()

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['bids'] = PlaceBidSerializer(instance.bids.all(), many=True).data
        return context 


class ProductDetailsSerializer(serializers.ModelSerializer):
    total_bids = serializers.SerializerMethodField(method_name='get_total_bids')
    highest_bid = serializers.SerializerMethodField(method_name='get_highest_bid')
    winning_bid = serializers.SerializerMethodField(method_name='get_winning_bid')

    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "title",
            "slug",
            "thumbnail",
            "price",
            "ending_time",
            "description",
            'total_bids',
            'highest_bid',
            'winning_bid',
            "created_at",
        )

    def to_representation(self, instance):
        context = super().to_representation(instance)
        update_placed_bid_status(instance)
        context['user'] = {"email": instance.user.email, "phone": instance.user.phone}
        context['active'] = instance.available
        return context
    
    def get_total_bids(self, obj):
        return PlacedBid.objects.filter(product=obj).count()

    def get_highest_bid(self, obj):
        maximum = PlacedBid.objects.filter(product=obj).aggregate(Max('amount'))
        highest = maximum['amount__max'] if maximum['amount__max'] else obj.price
        return highest
    
    def get_winning_bid(self, obj):
        bids = PlacedBid.objects.filter(
            product=obj,
            own=True
        )
        if bids.exists():
            bid = bids.first()
            data = {}
            data['user'] = bid.user.email
            data['max_amount'] = bid.amount
            return dict(data)
        else:
            return None
    


class PlaceBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacedBid
        fields = (
            "id",
            "product",
            "user",
            "amount",
            "bid_time",
        )

    def validate_amount(self, value):
         product = Product.objects.get(pk=self.get_initial().get('product'))
         less_amount = product.price > value
         bid = self.Meta.model.objects.filter(
             product=product,
             amount__gte=value
         )
         if less_amount:
             raise serializers.ValidationError(f"The product base price is {product.price}")
         
         if bid.exists():
            raise serializers.ValidationError(f"The minimum bidding price must be greater than {bid.first().amount}")
         
         return value
    
    def validate(self, validated_data):
         product = Product.objects.get(pk=validated_data.get('product').id)
         if not product.available:
            raise serializers.ValidationError("The bid is not active")
         return validated_data
    

class UserBidSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(read_only=True)
    bid_time = serializers.SerializerMethodField(method_name='get_bid_time')

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

    def get_bid_time(self, obj):
        print(obj.bid_time.strftime("%Y-%m-%d%H:%M"))
        return obj.bid_time.strftime("%Y-%m-%d %H:%M")
