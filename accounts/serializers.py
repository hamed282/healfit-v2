from rest_framework import serializers
from .models import User, AddressModel, CurrentAddressModel


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'trn_number', 'password',
                  'prefix_number']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserAddressSerializer(serializers.ModelSerializer):
    current_address = serializers.SerializerMethodField()

    class Meta:
        model = AddressModel
        fields = ['id', 'address', 'additional_information', 'emirats', 'city', 'country', 'phone_number',
                  'current_address', 'prefix_number']

    def get_current_address(self, obj):
        if CurrentAddressModel.objects.filter(address=obj).exists():
            print(CurrentAddressModel.objects.filter(address=obj))
            return True
        return False


class CurrentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAddressModel
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company_name', 'trn_number',
                  'prefix_number']


class UserInfoChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'trn_number', 'prefix_number']
