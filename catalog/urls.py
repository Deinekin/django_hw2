from django.urls import path
from catalog.views import ProductListView, ContactsTemplateView, ProductDetailView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_view")
]
