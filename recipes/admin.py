from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin configuration for Recipe model"""
    
    list_display = ['name', 'category', 'calories', 'preparation_time', 'cooking_time', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'ingredients']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('Content', {
            'fields': ('ingredients', 'instructions')
        }),
        ('Nutritional Information', {
            'fields': ('calories', 'protein', 'carbs', 'fat')
        }),
        ('Time & Servings', {
            'fields': ('preparation_time', 'cooking_time', 'servings')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )