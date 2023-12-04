from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.views import LoginView
from .forms import SignUpUserForm, CustomAuthenticationForm, PerfilForm, SignUpAdmUserForm
from events.models import Perfil
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class UserSignUpView(generic.CreateView):
    form_class = SignUpUserForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
    def get(self, request):
        form = SignUpUserForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = SignUpUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['cadastro_username'] = user.username
            request.session['cadastro_password'] = form.cleaned_data['password1']
            if 'is_staff' in request.POST:
                return redirect('adm')
            else:
                user.save()
                return redirect('login')
        return render(request, self.template_name, {'form': form})

class StaffSignUpView(generic.DetailView):
    form_class = SignUpAdmUserForm
    template_name = "registration/signup_adm.html"
    success_url = reverse_lazy('login')
    def get(self, request):
        form = SignUpAdmUserForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = SignUpAdmUserForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('payment_file')
            username = request.session.get('cadastro_username')
            password = request.session.get('cadastro_password')
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

class UserEditView(generic.UpdateView):
    form_class = PerfilForm
    template_name = "registration/edit.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        # Tenta obter o perfil do usuário atual
        perfil = Perfil.objects.filter(user=self.request.user)
        if perfil.exists():
            # Se o perfil existir, retorna o perfil
            return perfil.first()
        else:
            # Se o perfil não existir, cria um novo perfil
            return Perfil(user=self.request.user)