from django.contrib import admin
from .models import FoodLog

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    """Admin configuration for FoodLog model"""
    
    list_display = ['user', 'food_name', 'meal_type', 'calories', 'date', 'time']
    list_filter = ['meal_type', 'date', 'user']
    search_fields = ['food_name', 'user__email']
    date_hierarchy = 'date'