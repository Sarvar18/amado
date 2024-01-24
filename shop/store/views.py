from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Subcategory
from django.core.paginator import Paginator
from .forms import ReviewForm


# Create your views here.

def home_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/index.html', context)


def shop_view(request):
    query = request.GET.get('sort')

    if not query:
        products = Product.objects.filter(quantity__gte=0)
    else:
        products = Product.objects.filter(quantity__gte=0).order_by(query)

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products
    }
    return render(request, 'store/shop.html', context)


def subcategory_products(request, slug):
    query = request.GET.get('sort')
    subcategory = Subcategory.objects.get(slug=slug)

    if not query:
        products = Product.objects.filter(subcategory=subcategory, quantity__gt=0)
    else:
        products = Product.objects.filter(subcategory=subcategory, quantity__gt=0).order_by(query)

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.author = request.user
            form.save()
            return redirect('store:detail', product.slug)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'form': form,
        'reviews': reviews,
    }

    return render(request, 'store/detail.html', context)
