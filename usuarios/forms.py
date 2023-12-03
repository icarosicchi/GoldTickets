from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from events.models import Perfil


class SignUpUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=50, label='Primeiro nome')  
    last_name = forms.CharField(max_length=50, label='Último nome')  
    cpf = forms.CharField(max_length=14, label='CPF')
    cidade = forms.CharField(max_length=100, label='Cidade')
    username = forms.CharField(max_length=100, label='Nome de Login')
    password1 = forms.CharField(max_length=100, label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Confirme sua senha', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'cidade', 'password1', 'password2']

from django import forms

class CadastroSegundaEtapaForm(forms.Form):
    informacao_adicional = forms.CharField(max_length=100, required=True)
    uploaded_file = forms.FileField(required=False)
    tornar_staff = forms.BooleanField(required=False)


class SignUpAdmUserForm(UserCreationForm):
    payment_file = forms.FileField(required=False, label='Pagamento PIX')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nome de Login')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'telefone', 'whatsapp', 'instagram']