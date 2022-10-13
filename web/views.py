from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView

from web.forms import RegisterForm, AuthorizationForm, ProductForm
from web.models import Product, User


# Create your views here.


def products_page(request):
    search = request.GET.get('search', None)
    my_products = request.GET.get('my_products', None)
    if search is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(description__icontains=search))
    if my_products and request.user.is_authenticated:
        products = products.filter(user=request.user)
    products = products.order_by('-created_at')
    return render(request, 'web/main.html', {
        'products': products,
        'search': search,
    })


def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    is_owner = False
    if product in Product.objects.filter(user=request.user):
        is_owner = True
    return render(request, 'web/product.html', {
        'product': product,
        'is_owner': is_owner,
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


@login_required
def add_product_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            product = form.save()
            return redirect('product', product.id)
    return render(request, 'web/add_product.html', {
        'form': form,
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('products')


class ProductMixin:
    template_name = 'web/add_product.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'product'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        return Product.objects.filter(user=self.request.user)

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        return reverse('product', args=(self.object.id,))


class ProductDeleteView(ProductMixin, DeleteView):
    template_name = 'web/delete_product.html'

    def get_success_url(self):
        return reverse('products')

    def get_context_data(self, **kwargs):
        return {'product': Product.objects.filter(id=self.object.id)}


