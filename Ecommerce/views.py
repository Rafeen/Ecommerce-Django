from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm, LoginForm, RegisterForm
from django.utils.http import is_safe_url



class HomeView(TemplateView):
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class AboutView(TemplateView):
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "About"
        return context


class ContactView(View):
    template_name = "contact/contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "title": "Contact",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        context = {
            "title": "Contact",
            "form": form
        }
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            "title": "Login",
            "form": form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                # Return an 'invalid login' error message.
                print("Error")
        return render(request, "auth/login.html", context)


class RegisterView(View):
    template_name = 'auth/register.html'
    User = get_user_model()

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            "title": "Register",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        context = {
            "title": "Register",
            "form": form
        }
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            self.User.objects.create_user(username=username, password=password, email=email)
        return render(request, self.template_name, context)

