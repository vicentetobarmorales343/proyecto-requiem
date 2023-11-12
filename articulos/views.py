import json
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decorators import *


# Create your views here.

@login_required
def products_page(req):
    if req.method == 'GET':
        response = requests.get('http://localhost:4000/api/Inventory/Products')
        if response.status_code == 200:
            products = response.json()

            return render(req, 'products.html', {'products': products})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve products from API'})


@login_required
@role_required
def productsEntry_page(request):
    if request.method == 'POST':
        sku = request.POST['sku']
        categoria = request.POST['category']
        nombre = request.POST['name']
        precio = request.POST['price']
        stock = request.POST['stock']
        descripcion = request.POST['description']
        image = request.POST['imageUrl']

        product = {
            'idcategoria': categoria,
            'SKU': sku,
            'nombre': nombre,
            'precio_venta': precio,
            'stock': stock,
            'descripcion': descripcion,
            'image': image,
        }

        response_fuq = requests.get(
            'http://localhost:4000/api/Inventory/Products')
        products = response_fuq.json()

        for i in products:
            if str(i['SKU']) == str(sku):
                sku_founded = i['SKU']
                print(sku_founded)
                return render(request, 'ingreso.html', {'sku_founded': sku_founded})
            else:
                product = {
                    'idcategoria': categoria,
                    'SKU': sku,
                    'nombre': nombre,
                    'precio_venta': precio,
                    'stock': stock,
                    'descripcion': descripcion,
                    'image': image,
                }

                response = requests.post(
                    'http://localhost:4000/api/Inventory/addProduct', data=json.dumps(product), headers={'Content-Type': 'application/json'})

                if response.status_code == 200:
                    # redirige a una nueva página si el ingreso es exitoso
                    return redirect('products')
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to submit the product from API'})

    else:
        # renderiza tu formulario si el método no es POST
        return render(request, 'ingreso.html')


@csrf_exempt
@login_required
@role_required
def deleteProduct(req, idarticulo):
    if req.method == 'DELETE':
        response = requests.delete(
            'http://localhost:4000/api/Inventory/deleteProduct/' + idarticulo)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete product'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@role_required
def updateProduct(req, idarticulo):
    id_articulo = getProduct(idarticulo)

    if req.method == 'POST':
        sku = req.POST['sku']
        categoria = req.POST['category']
        nombre = req.POST['name']
        precio = req.POST['price']
        stock = req.POST['stock']
        descripcion = req.POST['description']
        image = req.POST['imageUrl']

        product = {
            'idcategoria': categoria,
            'SKU': sku,
            'nombre': nombre,
            'precio_venta': precio,
            'stock': stock,
            'descripcion': descripcion,
            'image': image,
        }

        response = requests.put(
            'http://localhost:4000/api/Inventory/updateProduct/'+idarticulo, data=json.dumps(product), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return redirect('products')
        else:
            return JsonResponse({'status': 'error', 'message': 'Producto no actualizado', 'product': product})

    else:
        return render(req, 'editarProducto.html', {'idarticulo': id_articulo})


def getProduct(idarticulo):
    response = requests.get(
        'http://localhost:4000/api/Inventory/getProduct/'+idarticulo)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    else:
        return None


@login_required
def searchProduct(req):
    if req.method == "POST":
        searched = req.POST['search']
        response = requests.post(
            'http://localhost:4000/api/Inventory/searchProduct/'+searched)
        if response.status_code == 200:
            results = response.json()
            print(results)
            return render(req, 'searchedProduct.html', {'results': results})
        else:
            return render(req, 'searchedProduct.html', {'error': 'No se encontraron resultados'})
    else:
        return render(req, 'searchedProduct.html')
