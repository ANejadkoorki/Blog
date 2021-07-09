from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'firstApp'
urlpatterns = [
    path('', views.post_view, name='posts'),
    path('createPost/', views.create_post, name='create-post'),
    path('createCategory/', views.CreateCategory.as_view(), name='create-category'),
    path('updateCategory/<int:pk>/', views.UpdateCategory.as_view(), name='update-category'),
    path('like-post/<int:id>', views.like_post, name='like-post'),
    path('edit_post/<int:pk>', views.edit_post, name='edit-post'),
    path('post_detail/<int:pk>', views.ViewPost.as_view(), name='details'),
    path('category/<slug:category_slug>/', views.FilterPostByCategory.as_view(), name='post-by-category'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
