from rest_framework import serializers

from .models import Users, Houses


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['salary', 'name', 'date']


class HousesSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Houses
        fields = ['user', "adress", "cost"]



