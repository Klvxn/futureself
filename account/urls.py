from django.urls import path

from .views import delete_account, LoginView, LogoutView, ManageAccountView, SignUpView


# Urls
app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/manage/', ManageAccountView.as_view(), name='manage_account'),
    path('me/delete/', delete_account, name='delete_account'),
]
