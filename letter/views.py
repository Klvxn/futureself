from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeletionMixin
from django.views.decorators.http import require_http_methods

from django_htmx.http import HttpResponseLocation

from .forms import LetterForm
from .models import Letter


# Create your views here.
class HomeView(CreateView):

    form_class = LetterForm
    template_name = 'homepage.html'
    success_url = reverse_lazy('letter:my_letters')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        

@login_required
def get_my_letters(request):
    travelling = Letter.objects.filter(user=request.user, delivered=False)
    delivered = Letter.objects.filter(user=request.user, delivered=True)
    context = {'travelling_letters': travelling, 'delivered_letters': delivered}
    return render(request, 'my_letters.html', context)


class LetterDetailView(DeletionMixin, DetailView):

    model = Letter
    template_name = 'letter_detail.html'
    context_object_name = 'letter'
    success_url = reverse_lazy('letter:my_letters')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@login_required
@require_http_methods(["POST", "PUT"])
def update_letter_audience(request, pk):
    letter = get_object_or_404(Letter, id=pk, user=request.user)
    if letter.user != request.user:
        return HttpResponseForbidden
    if letter.audience == 'private':
        letter.audience = 'public, but as anon'
    elif letter.audience == 'public, but as anon':
        letter.audience = 'private'
    letter.save()
    messages.success(request, 'Changes saved!')
    return HttpResponseLocation(letter.get_absolute_url())


class LetterCreateView(LoginRequiredMixin, CreateView):

    form_class = LetterForm
    template_name = 'create_letter.html'
    success_url = reverse_lazy('letter:create_letter')

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating new letter!')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Letter submitted sucessfully!")
        return super().form_valid(form)


class PublicLettersView(ListView):

    context_object_name = 'public_letters'
    template_name = 'public_letters.html'
    queryset = Letter.objects.filter(audience='public, but as anon', delivered=True)
    paginate_by = 3
    