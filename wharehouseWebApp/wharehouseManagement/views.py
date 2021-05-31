from .parsejson import parse_inventory, parse_products
from django.shortcuts import get_object_or_404, redirect, render
from .models import PartsAmount
from .models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def products(request):
    """View with a list of products, it may have a button to sell(remove) a product,
    if the product is availble and the user is logged in"""
    return render(request, 'products.html', {'products': Product.objects.all()})

def product(request,product_id):
    """View with a product details, including its articles"""
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product, 'parts': PartsAmount.objects.filter(product=product)})

@require_POST
@login_required
def remove_product(request):
    """View for selling(removing) a product, after it's done it returns the products view"""
    product_id = request.POST['product_id']
    get_object_or_404(Product, pk=product_id).remove()
    response = redirect('products')
    return response

def upload_inventory(request):
    """View to upload a file with the inventory description, see inventory.json in the testData folder"""
    return render(request,'upload.html',{'form_action':'upload_inventory_file'})

def upload_products(request):
    """View to upload a file with the products description, see products.json in the testData folder"""
    return render(request,'upload.html',{'form_action':'upload_products_file'})


@require_POST
@login_required
def upload_inventory_file(request):
    """View called to process the invetory file uploaded, redirects to the product list when done"""
    json_string = request.FILES['file'].read()
    parse_inventory(json_string)
    response = redirect('products')
    return response


@require_POST
@login_required
def upload_products_file(request):
    """View called to process the products file uploaded, redirects to the product list when done"""
    json_string = request.FILES['file'].read()
    parse_products(json_string)
    response = redirect('products')
    return response
