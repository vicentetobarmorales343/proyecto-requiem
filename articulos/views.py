import json
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decorators import *
from datetime import datetime


# Create your views here.

@login_required
def products_page(req):
    if req.method == 'GET':
        response = requests.get('http://localhost:4000/api/Inventory/Products')
        if response.status_code == 200:
            products = response.json()

            for product in products:
                product['created_at'] = datetime.strptime(
                    product['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

            return render(req, 'products.html', {'products': products})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve products from API'})


@login_required
@role_required
def productsEntry_page(request):
    categorias = categories()

    if request.method == 'POST':
        sku = request.POST['sku']
        categoria = request.POST['category']
        nombre = request.POST['name']
        precio = request.POST['price']
        stock = request.POST['stock']
        descripcion = request.POST['description']
        created_by = request.POST['createdBy']
        # Change this line to match your form's file input name
        file = request.FILES.get('file')  # Changed from 'image' to 'file'
        
        # Add file validation
        if not file:
            return JsonResponse({
                'status': 'error',
                'message': 'No file was uploaded'
            }, status=400)

        # Create product data dictionary
        product_data = {
            'idcategoria': categoria,
            'SKU': sku,
            'nombre': nombre,
            'precio_venta': precio,
            'stock': stock,
            'descripcion': descripcion,
            'created_by': created_by,
        }
        
        # Create files dictionary with the correct key
        files = {
            'file': (file.name, file, file.content_type)  # Changed from 'image' to 'file'
        }

        try:
            response = requests.post(
                'http://localhost:4000/api/Inventory/addProduct',
                data=product_data,
                files=files
            )
            
            if response.status_code == 200:
                return redirect('products')
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'API Error: {response.text}',
                    'status_code': response.status_code
                }, status=400)
                
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Request failed: {str(e)}'
            }, status=500)

    return render(request, 'ingreso.html', {'categorias': categorias})






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
    categorias = categories()
    id_articulo = getProduct(idarticulo)

    if req.method == 'POST':
        # Create MultipartEncoder for proper file upload
        files = {}
        if 'file' in req.FILES:
            files = {'file': (
                req.FILES['file'].name,
                req.FILES['file'],
                req.FILES['file'].content_type
            )}

        # Create form data
        data = {
            'idcategoria': req.POST['category'],
            'SKU': req.POST['sku'],
            'nombre': req.POST['name'],
            'precio_venta': req.POST['price'],
            'stock': req.POST['stock'],
            'descripcion': req.POST['description'],
            'created_by': req.POST['createdBy']
        }
        
        print("Data:", data)

        if 'imageUrl' in req.POST:
            data['image'] = req.POST['imageUrl']

        # If there are files, use multipart
        if files:
            response = requests.put(
                f'http://localhost:4000/api/Inventory/updateProduct/{idarticulo}',
                files=files,
                data=data  # Send as form data, not JSON
            )
        else:
            # If no files, send as regular form data
            response = requests.put(
                f'http://localhost:4000/api/Inventory/updateProduct/{idarticulo}',
                json=data
            )

        if response.status_code == 200:
            return redirect('products')
        else:
            print("Error response:", response.text)  # Add this for debugging
            return JsonResponse({
                'status': 'error',
                'message': 'Producto no actualizado',
                'product': data
            })

    return render(req, 'editarProducto.html', {
        'idarticulo': id_articulo,
        'categorias': categorias
    })




def getProduct(idarticulo):
    response = requests.get(
        'http://localhost:4000/api/Inventory/getProduct/'+idarticulo)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    else:
        return None


def categories():
    response = requests.get(
        'http://localhost:4000/api/Inventory/Categories/')
    if response.status_code == 200:
        categorias = response.json()
        return categorias
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
            for product in results:
                product['created_at'] = datetime.strptime(
                    product['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
            return render(req, 'searchedProduct.html', {'results': results})
        else:
            return render(req, 'searchedProduct.html', {'error': 'No se encontraron resultados'})
    else:
        return render(req, 'searchedProduct.html')
