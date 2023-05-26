import form as form
from django_filters.rest_framework import DjangoFilterBackend
from requests import post
from rest_framework import status, viewsets, mixins, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from django.contrib.auth.models import User
from social_core.pipeline import user

from .pagination import PostPagination
from .permissions import UserOrReadOnly

from rest_framework import filters

from posts.serializers import ProfileSerializer


class GetPostInfoView(APIView):
    permission_classes = [UserOrReadOnly]
    http_method_names = ['get', 'head', 'post']
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    pagination_class = PostPagination

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        filter_backends = (filters.SearchFilter, filters.OrderingFilter)
        search_fields = ('^author',)#поиск по автору
        #ordering_fields = ('pub_date',) #сортировка по дате
        ordering = ('pub_date',)  # сортировка по дате по умолчанию
        return Response(serializer.data)


    def post(self, request):
        self.http_method_names.append("GET")

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            '''post.author_id = 1
            post.save()'''
            '''post = form.save(False)
            post.author = post.author_id
            post.save()'''
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#все посты
'''class GetPostInfoView(APIView):



    @api_view(['GET', 'POST'])
    def cat(request):
        if request.method == 'POST':
            serializer = PostSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,) #можно смотреть анонимно
    #permission_classes = [UserOrReadOnly] #свой пермишен'''






#профиль любого пользователя
class ProfileView(APIView):
    def get(self, request, username):
        l = str(username)
        user = User.objects.get(username=l)
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(instance=posts, many=True)
        return Response(serializer.data)


    permission_classes = [UserOrReadOnly]

#профиль активного
class ProfileYouView(APIView):
    def get(self, request):
        #userr = User.objects.get(username=User.username)
        userr = User.objects.get(username=self.request.user)
        posts = Post.objects.filter(author=userr)
        #print(User.username)
        #print(userr)
        serializer = PostSerializer(instance=posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.http_method_names.append("GET")
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













'''class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnlyPermission]'''
'''class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UpdateDeleteViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
#создает и получает экземпляр объекта
class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass'''