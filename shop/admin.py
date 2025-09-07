from django.contrib import admin
from shop import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_name", "image"]
    ordering = ["id"]
    search_fields = ["title"]
    list_per_page = 16


@admin.register(models.DesktopBanner)
class DesktopBannerAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_name", "image"]
    ordering = ["id"]
    search_fields = ["title"]
    list_per_page = 16


@admin.register(models.MobileBanner)
class MobileBannerAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_name", "image"]
    ordering = ["id"]
    search_fields = ["title"]
    list_per_page = 16
