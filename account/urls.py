from django.urls import path

from .views import delete_account, LoginView, LogoutView, ManageAccountView, SignUpView


# Urls
app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/manage/', ManageAccountView.as_view(), name='manage_account'),
    path('<int:pk>/delete/', delete_account, name='delete_account'),
]
