import base64

from django.core.files.base import ContentFile
from requests import post
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from posts.models import Post

from posts.models import Profile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:images'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
class PostSerializer(ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Post
        fields = ('text', 'pub_date', 'author', 'image')

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)

        instance.pub_data = validated_data.get(
            'pub_data', instance.pub_data
        )
        instance.image = validated_data.get('images', instance.image)
        instance.save()
        return instance



class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'password')

