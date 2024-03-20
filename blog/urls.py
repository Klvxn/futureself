from django.urls import path

from .views import BlogListView, BlogDetailView, BlogCreateView, BlogEditView, update_like


app_name = 'blog'
urlpatterns = [
    path('all/', BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/<int:year>/<int:month>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('like/<slug:slug>/', update_like, name='update_like'),
    path('<slug:slug>/<int:year>/<int:month>/edit/', BlogEditView.as_view(), name='blog_edit'),
]
