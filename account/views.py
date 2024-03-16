from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View

from .forms import UpdateUserForm, SignUpForm


# Create your views here.
class SignUpView(FormView):

    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('letter:my_letters')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        login(self.request, user)
        return super().form_valid(form)


class LoginView(Login):

    template_name = 'login.html'
    success_url = reverse_lazy('letter:my_letters')


class LogoutView(Logout):

    success_url = reverse_lazy('letter:home')
    
    def dispatch(self, request, *args,**kwargs):
        messages.info(request, 'You\'ve been logged out!')
        return super().dispatch(request, *args, **kwargs)


class ManageAccountView(LoginRequiredMixin, View):

    form_class = UpdateUserForm
    template_name = 'manage_account.html'

    def get(self, request):
        user = request.user
        form = self.form_class(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)
        
    def post(self, request):
        user = request.user
        form = self.form_class(instance=user, data=request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved!')
            return redirect(reverse('account:manage_account'))
        messages.error(request, 'Error saving changes!')
        return render(request, self.template_name, context)


@login_required
def delete_account(request, pk):
    user = request.user
    user.delete()
    messages.success(request, 'Account deleted!')
    return redirect('/')