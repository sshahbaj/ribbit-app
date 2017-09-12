from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import AuthenticateForm, UserCreateForm, RibbitForm
from .models import Ribbit


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        ribbit_form = RibbitForm()
        user = request.user
        ribbit_self = Ribbit.objects.filter(user=user.id)
        ribbit_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all)
        ribbits = ribbit_self | ribbit_buddies
        context = {
            'ribbit_form': ribbit_form,
            'user': user,
            'next_url': '/',
        }

        return render(request, 'buddies.html', context)

    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
        context = {
            'auth_form': auth_form,
            'user_form': user_form,
        }

        return render(request, 'home.html', context)