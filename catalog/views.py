from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from catalog.forms import ProductForm, VersionForm, ProductCategoryForm, ProductPublishedForm, ProductDescriptionForm
from catalog.models import Product, Version
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.services import get_products_from_cache


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

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        product = Product.objects.get(pk=self.kwargs.get("pk"))

        version = Version.objects.filter(product=product)

        active_versions = version.filter(current=True)

        if active_versions:
            self.object.version_name = active_versions.last().name
        context_data['object_list'] = product
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data["formset"] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data["formset"] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        object_ = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateDescriptionView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductDescriptionForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCategoryForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdatePublishedView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductPublishedForm
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
