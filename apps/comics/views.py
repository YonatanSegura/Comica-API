import uuid
from django.db.models import Q
from django.template.defaulttags import csrf_token

from api_comica.settings import INDEX_IMG
from apps.comics.serializers import ComicSerializer, CreateComicSerializer, CreateComicsUrlSerializer, \
    BasicComicSerializer
from status import status_data
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
from rest_framework.response import Response

from apps.comics.models import Comic, ComicsUrl


def hello_word(request):
    return render(request, 'index.html')


def get_comic(self, many):
    return ComicSerializer(self, many=many)


def last_comics(ind):
    comics = Comic.objects.filter(rewards__gt=1.0).exclude(state=0)
    data = []
    i = 0
    for comic in comics:
        if i < ind:
            data.append(comic)
        elif i:
            break
        i += 1
    return BasicComicSerializer(data, many=True)


def all_comics():
    comics = Comic.objects.all().exclude(state=0).order_by('-created_by')
    return BasicComicSerializer(comics, many=True)


@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        try:
            last_comic = last_comics(4)
            data = {'img': INDEX_IMG, 'lasted_comics': last_comic.data}

            return Response(data, status=status.HTTP_200_OK)

        except (ValueError, KeyError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def comic_list(request):
    if request.method == 'GET':
        comics = Comic.objects.all().exclude(state=0).order_by('-id')
        serializer = BasicComicSerializer(comics, many=True)
        array_comics = {"comics": serializer.data}
        return Response(array_comics)

    elif request.method == 'POST':
        serializer = CreateComicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def view_comic(request, uid):
    try:
        comic = Comic.objects.get(Q(uuid=uid) & Q(state__gte=1))
    except Comic.DoesNotExist:
        errors = {"error": "404 no se encuentra ese registro"}
        return Response(errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ComicSerializer(comic)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CreateComicSerializer(comic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        comic.delete()
        return Response(status=status.HTTP_200_OK)
