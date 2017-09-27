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
        '''
        user.profile will call the get_or_create function for the user, if the user exists then it will return the user.
        Then it will check who all the user follows by using the all method.
        So, the user.profile.follows.all() can also be written as:
        u = user.profile
        u.follows.all()
        In the line user__userprofile__in, the Ribbit model has OnetoOne relationship with User model and so does the
        UserProfile model hence the UserProfile model is the child of User model hence syntax of above lookup is:
        parent__ChildOfParent__(continues)
        '''
        ribbit_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all())
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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            # Success
            login(request, form.get_user())
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')