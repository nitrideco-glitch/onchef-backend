from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model with read-only access"""
    
    total_time = serializers.IntegerField(read_only=True)
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients', 'instructions', 
                 'calories', 'protein', 'carbs', 'fat', 'category', 'category_display',
                 'preparation_time', 'cooking_time', 'total_time', 'servings',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_category_display(self, obj):
        """Get human-readable category name"""
        return obj.get_category_display()
    
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