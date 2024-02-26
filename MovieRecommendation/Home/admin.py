from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
class AdditionalImageTabular(admin.TabularInline):
    model = Additional_image
class ProductAdmin(admin.ModelAdmin):
    inlines = [AdditionalImageTabular]

admin.site.register(Banner_area)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(Rating)
admin.site.register(Favorite)