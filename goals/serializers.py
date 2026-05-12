from rest_framework import serializers
from .models import Goal
from django.core.validators import MinValueValidator

class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal model with validation"""
    
    days_remaining = serializers.IntegerField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Goal
        fields = ['id', 'goal_type', 'period', 'target_value', 'current_value', 
                 'success_rate', 'start_date', 'end_date', 'created_at', 'updated_at',
                 'days_remaining', 'is_completed']
        read_only_fields = ['id', 'success_rate', 'created_at', 'updated_at', 
                           'days_remaining', 'is_completed']
    
    def validate_target_value(self, value):
        """Validate target value is positive"""
        if value <= 0:
            raise serializers.ValidationError("Target value must be greater than zero")
        return value
    
    def validate_current_value(self, value):
        """Validate current value is not negative"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Current value cannot be negative")
        return value
    
    def validate(self, data):
        """Validate that end date is after start date"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if self.instance is not None:
            start_date = start_date if start_date is not None else self.instance.start_date
            end_date = end_date if end_date is not None else self.instance.end_date

        if start_date is not None and end_date is not None and end_date <= start_date:
            raise serializers.ValidationError({
                'end_date': "End date must be after start date"
            })
        return data
    
    def create(self, validated_data):
        """Create goal with automatic user assignment"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update goal and recalculate success rate"""
        instance = super().update(instance, validated_data)
        instance.calculate_success_rate()
        return instance