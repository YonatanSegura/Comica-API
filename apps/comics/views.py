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
    comics = Comic.objects.all().exclude(state=0).order_by('-id')
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


@api_view(['GET'])
def comic_list(request):
    if request.method == 'GET':
        try:
            last_comic = last_comics(6)
            all_comic = all_comics()
            data = {'comics': all_comic.data}

            return Response(data, status=status.HTTP_200_OK)

        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def view_comic(request, uid=None):
    if request.method == 'GET':
        try:
            print(uid)
            if uid is None:
                return Response(status_data.HTTP_400_BAD_REQUEST([200, 'Not Found Param in URL']),
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    comic = Comic.objects.get(Q(uuid=uid) & Q(state__gte=1))
                    print(comic.rewards)
                    comics = get_comic(comic, False).data

                    return Response(comics, status=status.HTTP_200_OK)
                except:
                    return Response(status_data.HTTP_404_NOT_FOUND([100, uid]),
                                    status=status.HTTP_404_NOT_FOUND)

        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        try:
            data = request.data
            if 'comics_url' in data.keys():
                serializer = CreateComicSerializer(data=data)
                if serializer.is_valid():
                    serializer = serializer.save()
                    for urls in data['comics_url']:
                        urls['comic'] = serializer.id
                        urls['uuid'] = str(uuid.uuid4())
                        print(urls)
                        serializer2 = CreateComicsUrlSerializer(data=urls)
                        if serializer2.is_valid():
                            serializer2.save()
                        else:
                            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(serializer2.errors)]),
                                            status=status.HTTP_400_BAD_REQUEST)
                    all = Comic.objects.get(pk=serializer.pk)
                    all = ComicSerializer(all, many=False)
                    return Response(all.data, status=status.HTTP_200_OK)
                else:
                    return Response(status_data.HTTP_400_BAD_REQUEST([200, str(serializer.errors)]),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    status_data.HTTP_400_BAD_REQUEST(
                        [200, "an array of 'comics_url' was expected in the request data"]),
                    status=status.HTTP_400_BAD_REQUEST)

        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print('paso aqui')
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            data = request.data
            if uid is None:
                return Response(status_data.HTTP_400_BAD_REQUEST([200, 'Not Found Param in URL']),
                                status=status.HTTP_400_BAD_REQUEST)
            comic = Comic.objects.get(Q(uuid=uid) & Q(state__gte=1))
        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = CreateComicSerializer(comic, data=data, partial=True)
            if serializer.is_valid():
                serializer = serializer.save()
                if 'comics_url' in data.keys():
                    for urls in data['comics_url']:
                        print(urls)
                        comic_url = ComicsUrl.objects.get(Q(uuid=urls['uuid']) & Q(state__gte=1))
                        serializer2 = CreateComicsUrlSerializer(comic_url, data=urls, partial=True)
                        if serializer2.is_valid():
                            serializer2.save()
                        else:
                            return Response(status_data.HTTP_400_BAD_REQUEST([200, serializer2.errors]),
                                            status=status.HTTP_400_BAD_REQUEST)
                all = Comic.objects.get(pk=serializer.pk)
                all = ComicSerializer(all, many=False)
                return Response(all.data, status=status.HTTP_200_OK)
            else:
                if 'comics_url' in data.keys():
                    for urls in data['comics_url']:
                        print(urls)
                        comic_url = ComicsUrl.objects.get(Q(uuid=urls['uuid']) & Q(state__gte=1))
                        serializer2 = CreateComicsUrlSerializer(comic_url, data=urls, partial=True)
                        if serializer2.is_valid():
                            serializer2.save()
                        else:
                            return Response(status_data.HTTP_400_BAD_REQUEST([200, serializer2.errors]),
                                            status=status.HTTP_400_BAD_REQUEST)
                    all = Comic.objects.get(pk=comic.pk)
                    all = ComicSerializer(all, many=False)
                    return Response(all.data, status=status.HTTP_200_OK)

                return Response(status_data.HTTP_400_BAD_REQUEST([200, serializer.errors]),
                                status=status.HTTP_400_BAD_REQUEST)

        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status_data.HTTP_400_BAD_REQUEST([100]), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            print(uid)
            if uid is None:
                return Response(status_data.HTTP_400_BAD_REQUEST([200, 'Not Found Param in URL']),
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    comic = Comic.objects.get(uuid=uid)
                    comic.delete()
                    return Response(status=status.HTTP_200_OK)
                except:
                    return Response(status_data.HTTP_404_NOT_FOUND([100, uid]),
                                    status=status.HTTP_404_NOT_FOUND)

        except (KeyError, ValueError, TypeError) as err:
            return Response(status_data.HTTP_400_BAD_REQUEST([200, str(err)]), status=status.HTTP_400_BAD_REQUEST)
