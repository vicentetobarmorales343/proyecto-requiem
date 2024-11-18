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
        username = req.POST['username']  
        password = req.POST['password']

        try:
            # Send the credentials in the request body
            response = requests.post(
                'http://localhost:4000/api/Inventory/login',
                json={
                    'rut': username,  # Match the API's expected field name
                    'password': password
                }
            )
            
            # Check if the request was successful
            if response.status_code == 201:  # Your API returns 201 on success
                user_data = response.json()
                user = user_data.get('user')
                
                if user:
                    # Store user data in session
                    req.session['login_status'] = True
                    req.session['username'] = user['nombre']
                    req.session['role'] = user['idrol']
                    req.session['rut'] = user['rut']
                    req.session.save()
                    return redirect('home')
                
            # If response wasn't successful or user data is invalid
            return render(req, 'login.html', {
                'message': 'Contraseña y/o rut incorrecto'
            })

        except requests.exceptions.RequestException as e:
            # Handle API connection errors
            print(f"API Error: {str(e)}")
            return render(req, 'login.html', {
                'message': 'Error de conexión con el servidor'
            })

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
            if response.status_code == 200 | response.status_code == 201:
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
