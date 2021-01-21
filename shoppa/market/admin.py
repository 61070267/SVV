from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Category, SubCategory

# Register your models here.
class SubCategoryAdmin(admin.StackedInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SubCategoryAdmin]

admin.site.register(Permission)

admin.site.register(Category, CategoryAdmin)