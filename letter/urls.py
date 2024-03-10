from django.urls import path

from .views import get_my_letters, update_letter, HomeView, PublicLettersView, LetterCreateView, LetterDetailView


app_name = 'letter'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my/letters/', get_my_letters, name='my_letters'),
    path('letters/<uuid:pk>/', LetterDetailView.as_view(), name='letter_detail'),
    path('letters/create/', LetterCreateView.as_view(), name='create_letter'),
    path('letters/<uuid:pk>/update/', update_letter, name='update_letter'),
    path('letters/audience/public/', PublicLettersView.as_view(), name='public_letters'),
]
