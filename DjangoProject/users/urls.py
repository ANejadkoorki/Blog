from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('Login/', views.login_view, name='login'),
    path('Logout/', views.logout_view, name='logout'),
    path('profile/edit', views.EditUserProfile.as_view(), name='edit-profile')
]
