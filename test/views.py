import json
import os
import uuid
from rest_framework import viewsets, status
from test.serializers import UsersSerializer, HousesSerializer
from test.input_serializers import UsersInputSerializer, HousesInputSerializer
from test.models import Users, Houses
from rest_framework.response import Response

from rest_framework.views import APIView
from datetime import datetime
from django.conf import settings


class UsersViewset(APIView):
    def get(self, request):
        if request.query_params.get('all'):
            users = Users.objects.all()
            return Response({"users": UsersSerializer(users, many=True).data, })
        elif request.query_params.get('user_id'):
            user = Users.objects.filter(pk=request.query_params.get('user_id')).first()
            if not user:
                return Response({'reason': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"user": UsersSerializer(user).data})

    def put(self, request):
        input_serializer = UsersInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        request_data = input_serializer.validated_data
        user = Users.objects.filter(pk=request_data.get("id")).first()
        if not user:
            return Response({'reason': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request_data.get('name'):
                user.name = request_data.get('name')
            if request_data.get('salary') and request_data.get('salary') % 123 > 1 and \
                    user.name.lower()[0] in ['a', 'o', 'u', 'e', 'i', 'y']:
                user.salary = request_data.get('salary') * 2
            if request_data.get('date'):
                date_str = request_data.get('date').strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                date_milli = date.timestamp() * 1000
                if date_milli > 43200000:
                    user.date = request_data.get('date').replace(year=1990, month=1, day=1)
        user.save()
        return Response({"user": UsersSerializer(user).data, })

class HousesViewset(APIView):
    def get(self, request):
        houses = Houses.objects.all()
        if request.query_params.get('user'):
            houses = Houses.objects.filter(user=request.query_params.get('user'))

        elif request.query_params.get('all'):
            houses = Houses.objects.all()
        return Response({"houses": HousesSerializer(houses, many=True).data, })

    def post(self, request):
        input_serializer = HousesInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        request_data = input_serializer.validated_data
        user = Users.objects.get(pk=request_data.get("user"))
        house = Houses.objects.create(
            user=user,
            adress=request_data.get("adress"),
            cost=request_data.get("cost"),
        )
        house.save()
        return Response(HousesSerializer(house).data)

    def put(self, request):
        input_serializer = HousesInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        request_data = input_serializer.validated_data
        house = Houses.objects.filter(pk=request_data['id']).first()
        user = Users.objects.get(pk=request_data.get("user"))
        if not house:
            return Response({'reason': 'house does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request_data.get('user'):
                house.user = user
            if request_data.get('adress'):
                house.address = request_data.get('adress')
            if request_data.get('cost'):
                house.cost = request_data.get('cost')
        house.save()
        return Response({"house": HousesSerializer(house).data, })

    def delete(self, request):
        input_serializer = HousesInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        request_data = input_serializer.validated_data
        delete_house = Houses.objects.filter(pk=request_data['id']).first()
        if not delete_house:
            return Response({'reason': 'house does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            delete_house.delete()
            return Response({'reason': 'deleted'}, status=status.HTTP_200_OK)


class FilesViewset(APIView):
    def get(self, request):
        path_files = os.listdir(settings.MAGIC_PATH)
        return Response({'reason': [os.path.join(settings.MAGIC_PATH, i) for i in path_files]},
                        status=status.HTTP_200_OK)

    def put(self, request):
        request_data = {}
        request_data.update(request.data)
        if request.query_params.get('file'):
            with open(os.path.join(settings.MAGIC_PATH, "{}.json".format(request.query_params.get('file'))), "w") as f:
                f.write(json.dumps(request.data))
        return Response({'reason': 'recorded'}, status=status.HTTP_200_OK)

    def delete(self, request):
        file = request.query_params.get('file')
        if not file:
            return Response({'reason': 'file not found'}, status=status.HTTP_400_BAD_REQUEST)
        os.remove(os.path.join(settings.MAGIC_PATH, f'{file}.json'))
        return Response({'reason': 'deleted'}, status=status.HTTP_200_OK)


class PhotoViewset(APIView):
    def get(self, request):
        path_files = os.listdir(settings.PHOTO_PATH)
        return Response({'reason': path_files}, status=status.HTTP_200_OK)

    def post(self, request):
        file = request.FILES['file']
        filename = uuid.uuid4().hex
        file_path = os.path.join(settings.PHOTO_PATH, filename[0:2], filename[2:4], filename[4:6])
        if file.size <= settings.MAX_SIZE:
            os.makedirs(file_path, exist_ok=True)
            with open(os.path.join(file_path, filename), "wb") as f:
                f.write(file.read())
        return Response({'reason': 'saved'}, status=status.HTTP_200_OK)


