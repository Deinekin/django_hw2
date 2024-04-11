from django.urls import path
from catalog.views import home, contacts, get_product
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("<int:pk>/", get_product, name="product_view")
]
