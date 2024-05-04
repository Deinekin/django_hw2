from django.urls import path
from catalog.views import ProductListView, ContactsTemplateView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_view"),
    path('create/', ProductCreateView.as_view(), name="create_product"),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name="update_product"),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
