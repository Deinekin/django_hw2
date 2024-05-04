from config import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название категории')
    description = models.TextField(verbose_name='описание категории')

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='название продукта')
    description = models.TextField(verbose_name='описание продукта')
    image_preview = models.ImageField(upload_to='product_photos/', verbose_name='фото', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='категория', **NULLABLE)
    price_per_product = models.FloatField(default=0.0, verbose_name='цена')
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='дата обновления', auto_now=True)
    # manufactured_at = models.DateField(verbose_name='дата производства продукта', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f"{self.category} {self.name} {self.price_per_product}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="продукт")
    number = models.PositiveIntegerField(verbose_name="номер версии")
    name = models.CharField(max_length=150, verbose_name="название версии")
    current = models.BooleanField(default=True, verbose_name="признак текущей версии")

    def __str__(self):
        return f"{self.name} {self.number}"

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"
