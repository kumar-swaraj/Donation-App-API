from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Donation


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    fields = ['id', 'name', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-id']
    date_hierarchy = 'created_at'


@admin.register(Donation)
class DonationAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_active']
    list_filter = ['categories', 'created_at']
    search_fields = ['title']
    fields = ['id', 'title', 'categories', 'amount', 'image', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-id']
    date_hierarchy = 'created_at'
