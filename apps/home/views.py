from django.contrib.auth import authenticate, login
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def home(request: WSGIRequest) -> HttpResponse:
    return render(
        request,
        'home/home.html',
        {
            'links': [
                {'name': 'Admin', 'url': '/admin/'},
                {'name': 'Categories', 'url': '/transactions/categories/'},
                {'name': 'Transactions', 'url': '/transactions/'},
                {'name': 'Users', 'url': '/users/me/'},
                {'name': 'Savings', 'url': '/savings/'},
                {'name': 'Savings Goals', 'url': '/savings/goals/'},
                {'name': 'Accounts', 'url': '/accounts/'},
                {'name': 'Documents', 'url': '/documents/'},
                {'name': 'Balance', 'url': '/transactions/balance/'},
            ]
        },
    )


def login_jwt(request: HttpRequest) -> HttpResponse:
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid username or password"

    return render(request, "home/login.html", {"error_message": error_message})
