from django.contrib import admin

from new_app import models

# Register your models here.
admin.site.register(models.Login)
admin.site.register(models.Register)

admin.site.register(models.CustomerAddress)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Brand)
admin.site.register(models.Products)
admin.site.register(models.VariantAdd)
admin.site.register(models.Variant)
admin.site.register(models.VariantValue)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Contact)
admin.site.register(models.Banner)

