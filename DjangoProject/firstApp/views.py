from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from . import models, forms


# Create your views here.


def post_view(request):
    if request.user.is_authenticated:
        my_posts = models.Post.objects.filter(creator=request.user)
        other_posts = models.Post.objects.exclude(creator=request.user)
    else:
        my_posts = models.Post.objects.all()
        other_posts = []

    return render(request,
                  template_name='firstApp/PostsTemplate.html',
                  context={
                      'object_list': my_posts,
                      'object_list2': other_posts,
                      'page_title': 'Posts',
                  }
                  )


@require_POST
@csrf_exempt
def like_post(request, id):
    """
    increments post`s likes
    """
    result = False
    # Main logic
    post_object = get_object_or_404(klass=models.Post, pk=id)
    post_object.likes += 1
    post_object.save()
    result = True
    # Response
    return JsonResponse({
        'result': result,
        'likes': post_object.likes,

    })


@login_required
def create_post(request):
    if not request.user.has_perm('firstApp.add_post'):
        raise PermissionDenied('Access Denied.')
    form_instance = forms.Postform()
    if request.method == 'POST':
        form_instance = forms.Postform(data=request.POST, files=request.FILES)
        if form_instance.is_valid():
            form_instance.instance.creator = request.user
            form_instance.save()
            return redirect('firstApp:posts')
    return render(request=request,
                  template_name='firstApp/PostFormTemplate.html',
                  context={
                      'form': form_instance,
                      'page_title': 'Create Post',
                  }
                  )


def edit_post(request, pk):
    """
    edit a post
    """
    post_instance = get_object_or_404(klass=models.Post, pk=pk)
    if not post_instance.creator == request.user:
        return HttpResponseForbidden('Access Denied.')
    if request.method == 'POST':
        form_instance = forms.Postform(instance=post_instance, data=request.POST, files=request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request, 'Saved Successfully! ')
            return redirect('firstApp:posts')
    else:
        # the GET method
        form_instance = forms.Postform(instance=post_instance)
        # instance argument get an model object
        # to Fill in the post blanks you can also
        # set your initial data with initial dictionary
        return render(
            request,
            template_name='firstApp/PostFormTemplate.html',
            context={
                'form': form_instance,
                'page_title': f'Edit post #{post_instance.pk}'
            },

        )


class CreateCategory(PermissionRequiredMixin, CreateView):
    model = models.Category
    fields = (
        'name',
        'slug',
    )
    success_url = reverse_lazy('firstApp:posts')
    template_name = 'firstApp/CategoryFormTemplate.html'
    extra_context = {
        'page_title': 'Create A Category'
    }
    permission_required = 'firstApp.add_category'


class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = models.Category
    fields = (
        'name',
        'slug',
    )
    success_url = reverse_lazy('firstApp:posts')
    template_name = 'firstApp/CategoryFormTemplate.html'


class ViewPost(DetailView):
    model = models.Post
    template_name = 'firstApp/PostDetailsTemplate.html'


class FilterPostByCategory(ListView):
    model = models.Post
    template_name = 'firstApp/PostsTemplate.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        # .kwargs includes url variables for example in this view <slug:category_slug>
        qs = super().get_queryset()
        qs = qs.filter(categories__slug=category_slug)
        # in filtering we start with a field(categories) and
        # continue with lookups likes another field in other
        # databases like (__slug) here or something like (__contains) and ...

        return qs
