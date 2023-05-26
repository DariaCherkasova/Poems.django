from django.urls import path, include


from . import views
#from .views import ShowProfilePageView

app_name = 'posts'
urlpatterns = [
    path('', views.index),
    path('group/', views.group, name='group'),
    path('posts/', views.posts_list),
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'), #на свой профиль
    path('posts/<int:post_id>/', views.post_detail, name='post_id'),
    path('create/', views.create_post, name='create_post'),
    path('profile/<str:username>/', views.profile_all, name='profile_all'), #на любой профиль

    ]