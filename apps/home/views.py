from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def home(request: WSGIRequest) -> HttpResponse:
    return render(
        request,
        'home/home.html',
        {
            'links': [
                {'name': 'Admin', 'url': '/admin/'},
                {'name': 'Login', 'url': '/api-auth/login/'},
                {'name': 'Categories', 'url': '/transactions/categories/'},
                {'name': 'Transactions', 'url': '/transactions/'},
                {'name': 'Users', 'url': '/users/me/'},
                {'name': 'Savings', 'url': '/savings/'},
                {'name': 'Accounts', 'url': '/accounts/'},
                {'name': 'Documents', 'url': '/documents/'},
                {'name': 'Balance', 'url': '/transactions/balance/'},
            ]
        },
    )
