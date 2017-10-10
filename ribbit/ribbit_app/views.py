from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AuthenticateForm, UserCreateForm, RibbitForm
from .models import Ribbit
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


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


@login_required
def submit(request):
    if request.method == 'POST':
        ribbit_form = RibbitForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if ribbit_form.is_valid():
            ribbit = ribbit_form.save(commit=False)
            ribbit.user = request.user
            ribbit.save()
            return redirect(next_url)
        else:
            return public(request, ribbit_form)
    return redirect('/')


@login_required
def public(request, ribbit_form=None):
    ribbit_form = ribbit_form or RibbitForm()
    ribbits = Ribbit.objects.reverse()[:10]
    context = {
        'ribbit_form': ribbit_form,
        'next_url': '/ribbits',
        'ribbits': ribbits,
        'username': request.user.username,
    }
    return render(request, 'public.html', context)


def get_latest(user):
    try:
        return user.ribbit_set.order_by('-id')[0]
    except IndexError:
        return ""


@login_required
def users(request, username="", ribbit_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        ribbits = Ribbit.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            context ={
                'user': user,
                'ribbits': ribbits,
            }
            return render(request, 'user.html', context)
        context = {
            'user': user,
            'ribbits': ribbits,
            'follow': True,
        }
        return render(request, 'user.html', context)
    users = User.objects.all().annotate(Count('ribbit'))
    ribbits = map(get_latest, users)
    obj = zip(users, ribbits)
    ribbit_form = ribbit_form or RibbitForm()
    context = {
        'obj': obj,
        'next_url': '/users/',
        'ribbit_form': ribbit_form,
        'username': request.user.username,
    }
    return render(request, 'profiles.html', context)


@login_required
def follow(request):
    if request.method == 'POST':
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')