from django.contrib.auth import get_user_model

from rest_framework import serializers

from .utils import validate_bd_number

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['phone'].validators = [validate_bd_number]

    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            'phone',
            "password",
            "password2",
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password2(self, value):
        password1 = self.get_initial().get('password')
        
        if password1 and password1 != value:
            raise serializers.ValidationError("Passwords mismatched")
        
        return value
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            password=validated_data.get('password'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        
        return user

