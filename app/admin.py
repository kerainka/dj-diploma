from django.contrib import admin
from .models import Product, Review, Order, Collection, ProductPosition


class OrderInline(admin.TabularInline):
    model = ProductPosition


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id', 'status')
    readonly_fields = ('order_sum', 'id')

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        obj.save()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
