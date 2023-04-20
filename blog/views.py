from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.views.generic.edit import DeletionMixin

from .models import Blog
from .forms import BlogForm


# Create your views here.
class BlogListView(ListView):

    template_name = 'blog_list.html'
    queryset = Blog.objects.filter(status='published')
    context_object_name = 'blogs_list'


class BlogDetailView(DeletionMixin, DetailView):

    model = Blog
    template_name = 'blog_detail.html'
    success_url = reverse_lazy('blog:blog_list')
    context_object_name = 'blog'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().writer:
            return HttpResponseForbidden()
        messages.success(request, 'Your blog has been deleted!')
        return super().post(request, *args, **kwargs)

    
class BlogCreateView(LoginRequiredMixin, CreateView):

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_create')
    template_name = 'blog_create.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Error in submitting blog.')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, 'Your post has been submitted for review.')
        return super().form_valid(form)


class BlogEditView(LoginRequiredMixin, UpdateView):

    model = Blog
    form_class = BlogForm
    template_name = 'blog_edit.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().writer:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().writer:
            return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, 'Changes saved!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()
