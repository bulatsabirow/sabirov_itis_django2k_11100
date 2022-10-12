from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from web.forms import RegisterForm, AuthorizationForm, ProductForm
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


def authorization_view(request):
    form = AuthorizationForm()
    message = None
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = 'Введённые данные неверны!'
            else:
                login(request, user)
                return redirect('products')

    return render(request, 'web/authorization.html', {
        'form': form,
        'message': message,
    })


def add_product_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            pass
    return render(request, 'web/add_product.html', {
        'form': form,
    })



