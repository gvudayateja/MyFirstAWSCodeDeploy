from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
