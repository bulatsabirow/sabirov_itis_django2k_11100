from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from web.forms import RegisterForm
from web.models import Product, User


# Create your views here.


def products_page(request):
    search = request.GET.get('search', None)
    if search is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(description__icontains=search))
    products = products.order_by('-created_at')
    return render(request, 'web/main.html', {
        'products': products,
        'search': search,
    })


def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'web/product.html', {
        'product': product,
    })


def registration_view(request):
    form = RegisterForm()
    is_registered = False
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            is_registered = True

    return render(request, 'web/registration.html', {
        'form': form,
        'is_registered': is_registered,
    })

