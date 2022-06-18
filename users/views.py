from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, AddEntryForm


def registerView(request):
    if request.user.is_authenticated:
        return redirect("main")

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data["username"]
            messages.success(
                request, f"Felicidades, {user}! Ya puedes iniciar sesión."
            )

            return redirect("login")

    context = {"form": form}

    return render(request, "register.html", context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect("main")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("main")
        else:
            messages.info(request, "El usuario o la contaseña son incorrectos")

    return render(request, "login.html")


def logoutUserView(request):
    logout(request)
    return redirect("login")


def addEntryView(request):
    if not request.user.is_staff:
        return redirect("main")

    form = AddEntryForm()
    toast_title = ""
    icon = "success"
    toast_background = "#CDF8B8"

    if request.method == "POST":
        form = AddEntryForm(request.POST)
        toast_title = form.save()
        if "unique" in form.errors.keys():
            toast_title = form.errors["unique"]
            icon = "error"
            toast_background = "#F8BEB8"

    if not toast_title and not icon:
        toast_title = ""

    context = {"form": form, "toast_title": toast_title, "icon": icon, "toast_background": toast_background}
    return render(request, "add_entry.html", context)
