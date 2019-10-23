from django.urls import path

from apps.comics.views import comic_list, view_comic

app_name = 'comics'

urlpatterns = [

    #path('comics/', view_comic, name='comic'),
    path('comics/<str:uid>', view_comic, name='comic'),
    path('comics/', comic_list, name='comic_list'),
]
