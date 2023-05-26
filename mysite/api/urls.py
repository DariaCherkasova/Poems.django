from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from . import views


app_name = 'api'

urlpatterns = [
    path('posts/', views.GetPostInfoView.as_view()),
    path('api-token-auth/', obtain_auth_token),
    path('profile/', views.ProfileYouView.as_view()),
    path('profile/<str:username>/', views.ProfileView.as_view()),


    ]
