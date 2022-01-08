from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.account_register_new_user, name='registration'),
    path('profile/<int:profile_id>/', views.account_profile, name='account_profile')
]