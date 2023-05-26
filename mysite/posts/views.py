from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets

from .models import Post, User
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator #разбить посты на страницы

from .forms import PostForm, UserUpdateForm

from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic.detail import DetailView
from .models import Profile
from .serializers import PostSerializer
from rest_framework.decorators import action


#@login_required
def index(request):
    if request.user.is_authenticated:

        print(f"Пользователь:  {request.user.username}")
    else:
        print("Вы не зарегистрированы ")
    #template = 'posts/index.html'
    #title ='Лев Толстой'

    post_list=Post.objects.all().order_by('-pub_date')
    paginator=Paginator(post_list, 2)

    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    #posts=Post.objects.order_by('-pub_date')
    context = {
        #'title': title,
        #'text':'Это главная страница проекта Yatube',
        #'postss' : posts,
        'page_obj':page_obj,
    }
    return render(request, 'posts/index.html', context)

def group(request):
    template = 'posts/group.html'
    title='Группа'
    context = {
        'title': title,
        'text': 'Здесь будет информация о группах проекта Yatube',
    }
    return render(request, template, context)


# Страница со всеми постами
def posts_list(request,):
    template = 'posts/post_detail.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)

#проверка авторизации
def only_user_view(reguest):
    if not reguest.user.is_authenticated:
        return redirect('/auth/login')


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста

    context = {

    }
    return render(request, 'posts/post_id.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/posts/')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


'''class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'posts/profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context'''




#профиль активного пользователя
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        'posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'posts/profile.html', context)

#профиль любого пользователя
@login_required
def profile_all(request, username,):
    l = str(username)
    user = User.objects.get(username=l)

    context = {
        'posts': Post.objects.filter(author=user)
    }

    return render(request, 'posts/profile_all.html', context)







































'''class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get(self, request):
        queryset = Post.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = PostSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        post = kwargs.pop('post', False)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(instance, data=request.data, post=post)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    #обновляем
    def update1(self, request, *args, **kwargs):
        kwargs['post'] = True
        self.update(request,  *args, **kwargs)

    #удаление
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_update(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)'''
