from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html', {
        'links': [
            {'name': 'Admin', 'url': '/admin/'},
            {'name': 'Login', 'url': '/api-auth/login/'},
            {'name': 'Transactions', 'url': '/transactions/'},
            {'name': 'Users', 'url': '/user-info/'},
            {'name': 'Savings', 'url': '/savings/'},
        ]
    })
