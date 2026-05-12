from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeFilter(filters.FilterSet):
    """Filter set for recipes"""
    
    min_calories = filters.NumberFilter(field_name="calories", lookup_expr='gte')
    max_calories = filters.NumberFilter(field_name="calories", lookup_expr='lte')
    min_protein = filters.NumberFilter(field_name="protein", lookup_expr='gte')
    category = filters.ChoiceFilter(choices=Recipe.CATEGORY_CHOICES)
    
    class Meta:
        model = Recipe
        fields = ['category', 'min_calories', 'max_calories', 'min_protein']

class RecipeListView(generics.ListAPIView):
    """List all recipes with filtering options (read-only)"""
    
    queryset = Recipe.objects.filter(is_active=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    filterset_class = RecipeFilter
    search_fields = ['name', 'description', 'ingredients']
    ordering_fields = ['calories', 'protein', 'carbs', 'fat', 'name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Apply additional filtering based on query parameters"""
        queryset = super().get_queryset()
        
        # Search by name or ingredients
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(ingredients__icontains=search)
            )
        
        return queryset

class RecipeDetailView(generics.RetrieveAPIView):
    """Retrieve a single recipe (read-only)"""
    
    queryset = Recipe.objects.filter(is_active=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    lookup_field = 'pk'

class RecipeByCategoryView(generics.ListAPIView):
    """List recipes by category"""
    
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filter recipes by category from URL"""
        category = self.kwargs.get('category')
        return Recipe.objects.filter(category=category, is_active=True)

# Import models for Q objects
from django.db import models