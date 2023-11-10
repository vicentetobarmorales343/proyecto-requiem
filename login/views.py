from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from .decorators import *
import requests

# Create your views here.


@login_required
def home_page(req):
    username = req.session.get('username')
    context = {'username': username}
    return render(req, "home.html", context)


@redirect_if_logged_in
def login_page(req):
    if req.method == 'POST':
        username = req.POST['username']  # Keep this as 'username'
        password = req.POST['password']

        response = requests.get('http://localhost:4000/api/Inventory/Users')
        users = response.json()

        for user in users:
            # Change 'username' to 'rut' here
            if user['rut'] == username and user['password'] == password:
                # If the username and password match, return a success status
                req.session['login_status'] = True
                req.session['username'] = user['nombre']
                return redirect('home')

        # If no match was found after checking all users, return an error status
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})

    return render(req, "login.html")


def logout_view(request):
    if 'login_status' in request.session:
        del request.session['login_status']
        del request.session['username']
        request.session.flush()
    return redirect('login')


def users_view(req):
    return render(req, 'users.html')


def users_view(req):
    if req.method == 'GET':
        response = requests.get('http://localhost:4000/api/Inventory/Users')
        if response.status_code == 200:
            users = response.json()

            return render(req, 'users.html', {'users': users})
        else:
            return render(req, 'error.html', {'error': 'Failed to retrieve users from API'})
