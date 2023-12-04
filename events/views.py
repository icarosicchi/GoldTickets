from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from .models import Event, Comment, Category, Ticket, Payment
from django.views import generic
from .forms import CommentForm, EventForm, GetTicketsForm, PaymentForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object().author

@method_decorator(csrf_exempt, name='dispatch')
class EventListView(generic.ListView):
    model = Event
    template_name = 'events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_list'] = Event.objects.all()  
        return context

@method_decorator(csrf_exempt, name='dispatch')
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

@csrf_exempt
def user_events(request):
    if request.user.is_authenticated:
        user_events = Event.objects.filter(author_id=request.user.id)
        context = {'user_events': user_events}
        return render(request, 'events/user_events.html', context)
    else:
        return render(request, 'events/login.html')
  
@csrf_exempt  
def user_tickets(request):
    if request.user.is_authenticated:
        user_tickets = Ticket.objects.filter(client=request.user.id, sold=True)
        user_pre_tickets = Ticket.objects.filter(client=request.user.id, sold=False)
        context = {
            'user_tickets': user_tickets,
            'user_pre_tickets': user_pre_tickets,
        }
        return render(request, 'events/user_tickets.html', context)
    else:
        return render(request, 'events/login.html')

@method_decorator(csrf_exempt, name='dispatch')
class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.tickets_left = form.instance.total_tickets
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class EventUpdateView(generic.UpdateView, AuthorRequiredMixin):
    model = Event
    template_name = 'events/update.html'
    success_url = reverse_lazy('events:index')
    form_class = EventForm

@method_decorator(csrf_exempt, name='dispatch')
class EventDeleteView(LoginRequiredMixin, generic.DeleteView, AuthorRequiredMixin):
    model = Event
    success_url = reverse_lazy('events:index')  
    template_name = 'events/delete.html'

    def test_func(self):
        Event = self.get_object()
        return self.request.user == Event.author

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

@csrf_exempt
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

@csrf_exempt
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

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(generic.ListView):
    model = Category
    template_name = 'events/categories.html' 

@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'events/detail_category.html'

@csrf_exempt
def get_tickets(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = GetTicketsForm(request.POST)
    tickets_id = []
    if event.tickets_left > 0:
        if event.presale and event.sale_date >= timezone.now().date():
            if request.method == 'POST':
                form = GetTicketsForm(request.POST)
                if form.is_valid():
                    tickets_amount = form.cleaned_data['tickets_amount']
                    for i in range(tickets_amount):
                        ticket_number = event.waiting_tickets + 1
                        event.waiting_tickets = event.waiting_tickets + 1
                        new_ticket = Ticket.objects.create(event=event, client=request.user, number=ticket_number, sold=False)
                        event.save()
                    return redirect('events:user_tickets')
            else:
                form = GetTicketsForm()
        else:
            if request.method == 'POST':
                form = GetTicketsForm(request.POST)
                if form.is_valid():
                    tickets_amount = form.cleaned_data['tickets_amount']
                    for i in range(tickets_amount):
                        event.tickets_left = event.tickets_left - 1
                        event.save()
                        ticket_number = event.total_tickets - event.tickets_left
                        new_ticket = Ticket.objects.create(event=event, client=request.user, number=ticket_number, sold=True)
                        tickets_id.append(new_ticket.id)
                    tickets_id = {
                        'tickets': tickets_id,
                    }
                    url = reverse('events:payment', kwargs={'event_id': event_id}) + f'?{urlencode({"tickets_id": tickets_id})}'
                    return redirect(url)
                else:
                    form = GetTicketsForm()
    return render(request, 'events/get_ticket.html', {'event': event, 'form': form})

@csrf_exempt
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'events/ticket_detail.html', {'ticket': ticket})

@csrf_exempt
def payment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets_id = request.GET.get('tickets_id')
    form = PaymentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('payment_voucher')
            payment = form.save(commit=False)
            payment = Payment(tickets=tickets_id,ticket_amount=len(tickets_id),payment_voucher=uploaded_file)
            payment.save()
            return redirect('events:paid', event_id)
        else:
            form = PaymentForm()
    if tickets_id:
        context = {
            'event': event,
            'tickets_amount': len(tickets_id), 
            'total':len(tickets_id)*event.price, 
            'form': form}
    else:
        context = {
            'event': event,
            'tickets_amount': 0, 
            'total':0.00, 
        'form': form}
    return render(request, 'events/payment.html', context)

def paid(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/detail.html', {'event': event})

    