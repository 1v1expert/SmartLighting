# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from internal.forms import LoginForm, SignUpForm, PromodemForm
from core.models import Promodem, Group
from django.template import loader

from django.http import HttpResponse


@login_required(login_url="/login/")
def index_view(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def pages_view(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def promodem_view(request):
    template = loader.get_template('pages/promodem.html')
    return HttpResponse(template.render({'devices': Promodem.objects.all(), 'groups': Group.objects.all()}, request))


@login_required(login_url="/login/")
def promodem_detail_view(request, pk):
    msg = None
    success = False
    
    try:
        promodem = Promodem.objects.get(pk=pk)
    except:
        msg = f'Not found promodem with pk = {pk}'
    
    if request.method == "POST":
        form = PromodemForm(instance=promodem, data=request.POST)
        if form.is_valid():
            form.save()
            
            return redirect("/promodem/")
        
        else:
            msg = 'Form is not valid'
    else:
        form = PromodemForm(instance=promodem)
    
    return render(request, "pages/promodem_detail.html", {"form": form, "msg": msg, "success": success})
    
    # template = loader.get_template('pages/promodem.html')
    # return HttpResponse(template.render({'promodems': Promodem.objects.all()}, request))


def login_view(request):
    form = LoginForm(request.POST or None)
    
    msg = None
    
    if request.method == "POST":
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    
    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            
            msg = 'User created.'
            success = True

            # return redirect("/login/")
        
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    
    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


