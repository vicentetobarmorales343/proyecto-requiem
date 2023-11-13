import json
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decorators import *

# Create your views here.


@login_required
@role_required
def categories(req):
    categorias = None
    if req.method == 'GET':
        response = requests.get(
            'http://localhost:4000/api/Inventory/Categories/')
        if response.status_code == 200:
            categorias = response.json()
    if categorias:
        return render(req, 'categorias.html', {'categorias': categorias})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to retrieve categories from API'})


@login_required
@role_required
def addCategory(req):
    if req.method == 'POST':
        nombre = req.POST['nombre']
        categoria = {
            'nombre': nombre,
        }

        response_fuq = requests.get(
            'http://localhost:4000/api/Inventory/Categories')
        categories = response_fuq.json()

        name_founded = False
        for i in categories:
            if str(i['nombre']) == str(nombre):
                name_founded = True
                break

        if name_founded:
            return render(req, 'ingresoCategoria.html', {'name_founded': name_founded})
        else:
            response = requests.post(
                'http://localhost:4000/api/Inventory/addCategory/', data=json.dumps(categoria), headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('categories')
            else:
                return JsonResponse({'status': 'error', 'message': 'Categoría no ingresada', 'category': categoria})
    return render(req, 'ingresoCategoria.html')


@csrf_exempt
@login_required
@role_required
def deleteCategory(req, idcategoria):
    if req.method == 'DELETE':
        response = requests.delete(
            'http://localhost:4000/api/Inventory/deleteCategory/' + idcategoria)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete category'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@role_required
def updateCategory(req, idcategoria):
    categoria = getCategory(idcategoria)
    if req.method == 'POST':
        nombre = req.POST['nombre']
        category = {
            'nombre': nombre,
        }

        response_fuq = requests.get(
            'http://localhost:4000/api/Inventory/Categories')
        categories = response_fuq.json()

        name_founded = False
        for i in categories:
            if str(i['nombre']) == str(nombre):
                name_founded = True
                break

        if name_founded:
            return render(req, 'actualizarCategoria.html', {'name_founded': name_founded, 'categoria': categoria})
        else:
            response = requests.put(
                'http://localhost:4000/api/Inventory/updateCategory/'+idcategoria, data=json.dumps(category), headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('categories')
            else:
                return JsonResponse({'status': 'error', 'message': 'Categoría no actualizada', 'categoria': category})
    else:
        return render(req, 'actualizarCategoria.html', {'categoria': categoria})


def getCategory(idcategoria):
    response = requests.get(
        'http://localhost:4000/api/Inventory/Category/'+idcategoria)
    if response.status_code == 200:
        return response.json()
    else:
        return None
