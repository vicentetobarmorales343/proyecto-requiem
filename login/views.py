from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import requests
from decorators import *
import json
from datetime import datetime

# Create your views here.


@login_required
def home_page(req):
    return render(req, "home.html")


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
                req.session['role'] = user['idrol']
                req.session['rut'] = user['rut']
                req.session.save()
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


@login_required
@role_required
@admin_required
def users_view(req):
    if req.method == 'GET':
        response = requests.get('http://localhost:4000/api/Inventory/Users')
        if response.status_code == 200:
            users = response.json()

            for user in users:
                user['created_at'] = datetime.strptime(
                    user['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

            return render(req, 'users.html', {'users': users})
        else:
            return render(req, 'error.html', {'error': 'Failed to retrieve users from API'})


@login_required
@role_required
@admin_required
def usersEntry_page(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['name']
        cargo = request.POST['charge']
        contraseña = request.POST['password']

        user_entry = {
            'rut': rut,
            'nombre': nombre,
            'idrol': cargo,
            'password': contraseña,
        }

        response_fu = requests.get('http://localhost:4000/api/Inventory/Users')
        users = response_fu.json()

        for user in users:
            if user['rut'] == rut:
                return render(request, 'usersEntry.html', {'rut_founded': 'El identificador ya está en uso'})
        else:
            response = requests.post(
                'http://localhost:4000/api/Inventory/addUser', data=json.dumps(user_entry), headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('users')
            else:
                return JsonResponse({'status': 'error', 'message': 'Usuario no ingresado'})

    else:
        # renderiza tu formulario si el método no es POST
        return render(request, 'usersEntry.html')


@csrf_exempt
@login_required
@role_required
@admin_required
def deleteUser(request, user_rut):
    if request.method == 'DELETE':
        response = requests.delete(
            'http://localhost:4000/api/Inventory/deleteUser/' + user_rut)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete user'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@role_required
@admin_required
def updateUser(request, user_rut):

    user = getUser(user_rut)

    if request.method == 'POST':
        nombre = request.POST['name']
        cargo = request.POST['charge']
        contraseña = request.POST['password']

        user_entry = {
            'nombre': nombre,
            'idrol': cargo,
            'password': contraseña,
        }

        response = requests.put(
            'http://localhost:4000/api/Inventory/updateUser/'+user_rut, data=json.dumps(user_entry), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return redirect('users')
        else:
            return JsonResponse({'status': 'error', 'message': 'Usuario no actualizado'})

    else:
        return render(request, 'usersUpdate.html', {'user': user})


def getUser(user_rut):
    response = requests.get(
        'http://localhost:4000/api/Inventory/User/'+user_rut)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    else:
        return None
