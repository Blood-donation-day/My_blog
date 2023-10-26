from django.urls import path
from .views import SignupView, UserLoginView, UserLogoutView, UserUpdateView, user_profile
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup/',  SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('<str:email>/', user_profile, name='profile'),
]
