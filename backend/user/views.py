from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from urllib.parse import urlsplit, urlunsplit

from .models import Passenger
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('user:login')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # <== Убедись, что здесь именно 'home'
            else:
                messages.error(request, 'Неверный email или пароль.')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def home_view(request):
    print(">> Пользователь:", request.user.email if request.user.is_authenticated else "Аноним")
    return render(request, 'home.html')

# === Logout system ===

class LogoutView(TemplateView):
    http_method_names = ["post", "options"]
    template_name = "logged_out.html"
    extra_context = None
    next_page = None

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            "site": current_site,
            "site_name": current_site.name,
            "title": _("Вы вышли из аккаунта"),
            **(self.extra_context or {}),
        })
        return context

def logout_then_login(request, login_url=None):
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return LogoutView.as_view(next_page=login_url)(request)

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)
    login_url_parts = list(urlsplit(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[3], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[3] = querystring.urlencode(safe="/")
    return HttpResponseRedirect(urlunsplit(login_url_parts))
