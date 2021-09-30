from rest_framework import serializers
from rest_framework.fields import empty


class UsersInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    salary = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    date = serializers.DateTimeField(required=False)


class HousesInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    user = serializers.IntegerField()
    adress = serializers.CharField(max_length=256, required=False)
    cost = serializers.IntegerField(required=False)