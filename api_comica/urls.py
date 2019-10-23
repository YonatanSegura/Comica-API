from django.urls import path, include
from apps.comics.views import index

urlpatterns = [
    path('index', index),
    path('comica/v1/', include('apps.comics.urls')),
]