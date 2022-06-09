import imp
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm
from books.forms import BookForm

# Create your views here.
def registerView(request):

    if request.user.is_authenticated:
        return redirect('main')
        
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Felicidades, {user}! Ya puedes iniciar sesión.')        

            return redirect('login')

    context = {
            'form': form
    }

    return render(request, 'register.html', context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'El usuario o la contaseña son incorrectos')

    return render(request, 'login.html')


def logoutUserView(request):
    logout(request)
    return redirect('login')

def addEntryView(request):
    if not request.user.is_staff:
        redirect('main')

    form = BookForm

    
    context = {
        'form' : form
    }
    return render(request, 'add_entry.html', context)
