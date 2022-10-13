from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView, ListView, DetailView, UpdateView

from oxygen import settings
from web.forms import RegisterForm, AuthorizationForm, ProductForm
from web.models import Product, User


# Create your views here.

class ProductListView(ListView):
    template_name = 'web/main.html'
    context_object_name = 'products'

    def get_queryset(self):
        return self.filter_queryset(Product.objects.all())

    def filter_queryset(self, products):
        self.search = self.request.GET.get('search', None)
        if self.search is not None:
            products = products.filter(Q(name__icontains=self.search) |
                                       Q(description__icontains=self.search))
        products = products.order_by('-created_at')
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super().get_context_data(),
            'search': self.search
        }


class ProductUserListView(ProductListView, LoginRequiredMixin):
    template_name = 'web/my.html'
    redirect_field_name = 'authorization'
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        print(self.request.user.id)
        return self.filter_queryset(Product.objects.filter(user=self.request.user.id))


# def products_page(request):
#     search = request.GET.get('search', None)
#     if search is None:
#         products = Product.objects.all()
#     else:
#         products = Product.objects.filter(Q(name__icontains=search) |
#                                           Q(description__icontains=search))
#     products = products.order_by('-created_at')
#     return render(request, 'web/main.html', {
#         'products': products,
#         'search': search,
#     })


class ProductDetailView(DetailView):
    template_name = 'web/product.html'
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Product


# def product_view(request, id):
#     product = get_object_or_404(Product, id=id)
#     seller = User.objects.filter(id=product.user.id)[0].name
#     is_owner = False
#     if product in Product.objects.filter(user=request.user):
#         is_owner = True
#     return render(request, 'web/product.html', {
#         'product': product,
#         'is_owner': is_owner,
#         'seller': seller,
#     })

def registration_view(request):
    form = RegisterForm()
    is_registered = False
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            is_registered = True
            login(request, user)
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
                next_url = 'products'
                if 'next' in request.GET:
                    next_url = request.GET.get('next')
                return redirect(next_url)

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


class ProductUpdateView(ProductMixin, UpdateView, LoginRequiredMixin):
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'id': self.kwargs[self.slug_url_kwarg],
        }


class ProductDeleteView(ProductMixin, DeleteView, LoginRequiredMixin):
    template_name = 'web/delete_product.html'

    def get_success_url(self):
        return reverse('products')

    def get_context_data(self, **kwargs):
        return {'product': Product.objects.filter(id=self.object.id)}
