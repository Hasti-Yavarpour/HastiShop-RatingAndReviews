from django.contrib import admin
from django.shortcuts import redirect
from .models import (
    Brand, Category, SubCategory, Color, Unit,
    Material, Product, Image, ProductReview, ReviewModerationEntry
)

# ------------------ Review Moderation Link in Admin ------------------

@admin.register(ReviewModerationEntry)
class ReviewModerationAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('/shop/moderate-reviews/')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# ------------------ Product Review with Approval ------------------

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'rating', 'comment', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'created_at')
    search_fields = ('product__name', 'comment')
    actions = ['approve_selected']

    @admin.action(description='Approve selected reviews')
    def approve_selected(self, request, queryset):
        queryset.update(approved=True)

# ------------------ Register Other Models ------------------

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Unit)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(Image)
