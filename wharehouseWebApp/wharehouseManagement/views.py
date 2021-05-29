from .parsejson import parse_inventory, parse_products
from django.shortcuts import get_object_or_404, redirect, render
from .models import PartsAmount
from .models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def products(request):
    return render(request, 'products.html', {'products': Product.objects.all()})

def product(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product, 'parts': PartsAmount.objects.filter(product=product)})

@require_POST
@login_required
def remove_product(request):
    product_id = request.POST['product_id']
    get_object_or_404(Product, pk=product_id).remove()
    response = redirect('products')
    return response

def upload_inventory(request):
    print("upload_inventory")
    return render(request,'upload.html',{'form_action':'upload_inventory_file'})

def upload_products(request):
    return render(request,'upload.html',{'form_action':'upload_products_file'})


@require_POST
@login_required
def upload_inventory_file(request):
    json_string = request.FILES['file'].read()
    parse_inventory(json_string)
    response = redirect('products')
    return response


@require_POST
@login_required
def upload_products_file(request):
    json_string = request.FILES['file'].read()
    parse_products(json_string)
    response = redirect('products')
    return response
