from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.createUser),
    path('user/login/', views.login),
    path('user/check/', views.userCheck),
    path('profile/', views.ProfileView.as_view()),
]
