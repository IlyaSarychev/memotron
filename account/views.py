from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import AccountLoginForm


class LoginView(auth_views.LoginView):
    authentication_form = AccountLoginForm


@login_required
def account_profile(request):
    return render(request, 'account/profile/detail.html')