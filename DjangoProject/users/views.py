from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views.generic import UpdateView

from . import forms


# Create your views here.


def login_view(request):
    """logins the user !!!"""
    form_instance = forms.LoginForm()
    user = None
    if request.method == 'POST':
        form_instance = forms.LoginForm(data=request.POST)
        if form_instance.is_valid():
            username = form_instance.cleaned_data['username']
            password = form_instance.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # returns an user object
            if user is not None:
                # the user was found and authenticated
                login(request, user)
                next_url = request.GET.get('next', '/')
                if is_safe_url(next_url, settings.ALLOWED_HOSTS):
                    return redirect(next_url)
                else:
                    return redirect('/')
            else:
                # the user or password is invalid
                messages.error(request, 'username or password was incorrect')
    return render(request=request,
                  template_name='users/LoginTemplate.html',
                  context={
                      'form': form_instance,
                  },
                  )


def logout_view(request):
    """logout`s the users"""
    logout(request)
    messages.success(request, 'You`ve been loged out successfully!!!')
    return redirect('firstApp:posts')


# View Class
class EditUserProfile(LoginRequiredMixin, UpdateView):
    """
    updates a  user profile
    """
    model = get_user_model()  # this function returns user`s model
    fields = (
        'first_name',
        'last_name',
        'email',
    )
    template_name = 'users/UserFormTemplate.html'
    success_url = reverse_lazy('firstApp:posts')

    # reverse_lazy() is like {% url %} in template

    def get_object(self, queryset=None):
        return self.request.user
