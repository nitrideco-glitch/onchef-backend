from rest_framework import serializers
from .models import FoodLog
from django.core.validators import MinValueValidator

class FoodLogSerializer(serializers.ModelSerializer):
    """Serializer for Food Log with validation"""
    
    class Meta:
        model = FoodLog
        fields = ['id', 'food_name', 'meal_type', 'calories', 'protein', 'carbs', 'fat', 
                 'date', 'time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_calories(self, value):
        """Validate calories is not negative"""
        if value < 0:
            raise serializers.ValidationError("Calories cannot be negative")
        return value
    
    def validate_protein(self, value):
        """Validate protein is not negative"""
        if value < 0:
            raise serializers.ValidationError("Protein cannot be negative")
        return value
    
    def validate_carbs(self, value):
        """Validate carbs is not negative"""
        if value < 0:
            raise serializers.ValidationError("Carbs cannot be negative")
        return value
    
    def validate_fat(self, value):
        """Validate fat is not negative"""
        if value < 0:
            raise serializers.ValidationError("Fat cannot be negative")
        return value
    
    def create(self, validated_data):
        """Create food log with automatic user assignment"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)