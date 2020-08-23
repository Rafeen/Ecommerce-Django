from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic.base import TemplateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
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
            if request.is_ajax():
                return JsonResponse({"message": "Thank you for your submission"})

        if form.errors:
            errors = form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')
        return render(request, self.template_name, context)




