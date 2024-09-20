
from django.urls import path
from . import views
from .views import UserLoginView, user_logout_view, RegisterView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
]