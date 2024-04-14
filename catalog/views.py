from django.shortcuts import render

from catalog.models import Product
from django.views.generic import DetailView, ListView, TemplateView


#
# def home(request):
#     products = Product.objects.all()
#     context = {
#         "object_list": products
#     }
#     return render(request, "catalog/home.html", context)
#
#
# def get_product(request, pk):
#     product = Product.objects.get(pk=pk)
#     context = {
#         "object": product
#     }
#     return render(request, "catalog/product.html", context)


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         print(f"Имя: {name} Телефон: {phone} Сообщение: {message}")
#     return render(request, 'catalog/contacts.html')


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"
