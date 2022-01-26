from django import urls
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.account_register_new_user, name='registration'),
    path('profile/', views.account_profile, name='self_account_profile'),
    path('profile/<int:profile_id>/', views.account_profile, name='account_profile'),
    path('profile/photo/change/', views.profile_change_photo, name='profile_change_photo'),
    path('ajax-search-profiles', views.ajax_search_profiles, name='ajax_search_profiles'),
]