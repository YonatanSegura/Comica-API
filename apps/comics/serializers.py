from rest_framework import serializers

from apps.comics.models import Comic, ComicsUrl


class ComicsUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicsUrl
        fields = [
            'uuid',
            'url',
            'index'
        ]


class CreateComicsUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicsUrl
        fields = [
            'uuid',
            'comic',
            'url',
            'index'
        ]


class ComicSerializer(serializers.ModelSerializer):
    comics_url = ComicsUrlSerializer(many=True)

    class Meta:
        model = Comic
        fields = [
            'uuid',
            'comic',
            'author',
            'url',
            'description',
            'rewards',
            'comics_url'
        ]


class BasicComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = [
            'uuid',
            'comic',
            'author',
            'url',
            'description',
            'rewards'
        ]


class CreateComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = [
            'comic',
            'author',
            'url',
            'description',
            'rewards'
        ]
