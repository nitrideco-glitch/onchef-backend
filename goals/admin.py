from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """Admin configuration for Goal model"""
    
    list_display = ['user', 'goal_type', 'period', 'target_value', 'success_rate', 'start_date', 'end_date']
    list_filter = ['goal_type', 'period', 'start_date']
    search_fields = ['user__email', 'goal_type']
    readonly_fields = ['success_rate']