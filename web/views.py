from django.shortcuts import render

from web.models import Product


# Create your views here.


def products_page(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'web/main.html', {
        'products': products,
    })

