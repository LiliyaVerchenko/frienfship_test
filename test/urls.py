from django.urls import re_path

from test.views import UsersViewset, HousesViewset, FilesViewset, PhotoViewset

urlpatterns = [
    re_path('users/$', UsersViewset.as_view()),
    re_path('houses/$', HousesViewset.as_view()),
    re_path('files/$', FilesViewset.as_view()),
    re_path('photo/$', PhotoViewset.as_view()),
]
