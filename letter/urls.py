from django.urls import path

from . import views


app_name = 'letter'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('my/letters/', views.get_my_letters, name='my_letters'),
    path('letters/<uuid:pk>/', views.LetterDetailView.as_view(), name='letter_detail'),
    path('letters/create/', views.LetterCreateView.as_view(), name='create_letter'),
    path('letters/<uuid:pk>/update/', views.update_letter_audience, name='update_letter'),
    path('letters/audience/public/', views.PublicLettersView.as_view(), name='public_letters'),
    path('comment/new/<uuid:letter_id>/', views.get_comment_form),
    path('letters/<uuid:letter_id>/comment/new/', views.post_comment, name='post_comment'),
]
