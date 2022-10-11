from django.shortcuts import render, get_object_or_404

from web.models import Product


# Create your views here.


def products_page(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'web/main.html', {
        'products': products,
    })


def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'web/product.html', {
        'product': product,
    })

