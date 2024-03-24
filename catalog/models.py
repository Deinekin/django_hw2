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

    def __str__(self):
        return f"{self.category} {self.name} {self.price_per_product}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
