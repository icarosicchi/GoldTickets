from django import forms
from .models import Event, Comment, Category

class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    presale = forms.BooleanField()
    sale_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'location',
            'event_date',
            'price',
            'presale',
            'presale_tickets',
            'sale_date',
            'total_tickets',
            'photo_url',
            'categories'
        ]
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'location': 'Local',
            'event_date': 'Data do Evento',
            'price': 'Valor do Ingresso',
            'presale': 'Habilitar pré-venda?',
            'presale_tickets': 'Quantidade de ingressos na pré-venda',
            'sale_date': 'Data de início das vendas',
            'total_tickets' : 'Quantidade de ingressos',
            'photo_url': 'URL da foto',
            'categories': 'Categorias do Evento'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        labels = {
            'text': 'Comentário',
        }
