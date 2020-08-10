from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail


class GuestRegisterView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = GuestForm()
        context = {
            "title": "Guest",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = GuestForm(request.POST or None)
        context = {
            "title": "Guest",
            "form": form
        }
        next_ = request.POST.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_guest_email = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('account:register')
        return redirect('account:register')


class LoginView(View):
    template_name = 'accounts/login.html'

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
        next_ = request.POST.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('home')
            else:
                # Return an 'invalid login' error message.
                print("Error")
        return redirect('home')


class RegisterView(View):
    template_name = 'accounts/register.html'
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

