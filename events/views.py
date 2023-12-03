from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from .models import Event, Comment, Category
from django.views import generic
from .forms import CommentForm, EventForm
from django.contrib.auth.models import User
from django.utils import timezone

class EventListView(generic.ListView):
    model = Event
    template_name = 'events/index.html'

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        comments = event.comments.all().order_by('-post_date')
        context['comments'] = comments
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.pub_date = timezone.now()
            comment.save()
            return redirect('detailView', pk=event.pk)
        else:
            comments = event.comments.all().order_by('-pub_date')
            return render(request, 'events/detail.html', {'event': event, 'comments': comments, 'form': form})

class EventCreateView(generic.CreateView):
    model = Event
    template_name = 'events/create.html'
    success_url = reverse_lazy('events:index')
    form_class = EventForm
    def createEvent(request):
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.author = request.user
                event.tickets_left = event.total_tickets
                event.time = timezone.now()
                event.save()
                form.save_m2m()
                return redirect('detailView', pk=event.pk)
        else:
            form = EventForm()
        return render(request, 'events/create.html', {'form': form})

class EventUpdateView(generic.UpdateView):
    model = Event
    template_name = 'events/update.html'
    # success_url = reverse_lazy('events:index')
    form_class = EventForm

class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'events/delete.html'
    # success_url = reverse_lazy('events:index')
    form_class = EventForm

def search(request):
    query = request.GET.get('searched', '')
    events = Event.objects.filter(name__icontains=query)
    categories = Category.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'events': events,
        'categories': categories,
    }
    return render(request, 'events/search.html', context)

def create_comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment_author = request.user 
            comment_text = form.cleaned_data['text']
            comment = Comment(author=comment_author,
                            text=comment_text,
                            event=event)
            comment.save()
            return HttpResponseRedirect(
                reverse('events:detail', args=(event_id, )))
    else:
        form = CommentForm()
    context = {'form': form, 'event': event}
    return render(request, 'events/comment.html', context)   

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'events/categories.html' 

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'events/detail_category.html'

def buy_tickets(request, event_id):
    if request.user.is_authenticated and not request.user.is_staff:
        event = Event.objects.get(pk=event_id)
        event.tickets_left -= 1
        ticket_number = event.total_tickets - event.tickets_left
        new_ticket = Ticket.objects.create(event=event, user=request.user, number=ticket_number)
        # Adicione lógica adicional, como atualizar o carrinho de compras, processar o pagamento, etc.
        return render(request, 'events/buy_tickets.html')
    else:
        # O usuário não está autenticado, redirecione para a página de login ou exiba uma mensagem de erro.
        return render(request, 'registration/login.html')