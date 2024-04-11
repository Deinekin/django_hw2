from django.shortcuts import render
from catalog.models import Category, Product


def home(request):
    products = Product.objects.all()
    context = {
        "object_list": products
    }
    return render(request, "catalog/home.html", context)


def get_product(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        "object": product
    }
    return render(request, "catalog/product.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Имя: {name} Телефон: {phone} Сообщение: {message}")
    return render(request, 'catalog/contacts.html')
