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

from .forms import LetterForm, CommentForm
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
def current_user_letters(request):
    travelling = Letter.objects.filter(user=request.user, delivered=False)
    delivered = Letter.objects.filter(user=request.user, delivered=True)
    context = {'travelling_letters': travelling, 'delivered_letters': delivered}
    return render(request, 'my_letters.html', context)


class LetterDetailView(DeletionMixin, DetailView):

    model = Letter
    template_name = 'letter_detail.html'
    context_object_name = 'letter'
    success_url = reverse_lazy('letter:my_letters')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

def get_comment_form(request, letter_id):
    letter = get_object_or_404(Letter, id=letter_id)
    form = CommentForm()
    context = {'form': form, 'letter': letter}
    return render(request, 'partials/comment_form.html', context)


def post_comment(request, letter_id):
    letter = get_object_or_404(Letter, id=letter_id)
    form = CommentForm(request.POST)
    form.is_valid()
    comment = form.save(commit=False)
    comment.user = f'{request.user}' if request.user.is_authenticated else form.cleaned_data['user']
    comment.letter = letter
    comment.save()
    messages.success(request, 'Comment posted!')
    return HttpResponseLocation(letter.get_absolute_url())


@login_required
@require_http_methods(["POST"])
def update_letter_audience(request, pk):
    letter = get_object_or_404(Letter, id=pk, user=request.user)
    if letter.user != request.user:
        return HttpResponseForbidden
    if letter.audience == 'private':
        letter.audience = 'public, but as anon'
    elif letter.audience == 'public, but as anon':
        letter.audience = 'private'
    letter.save()
    return render(request, 'partials/audience.html', {'letter': letter})


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
    paginate_by = 10
    