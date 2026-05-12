from django.db import models
from django.core.validators import MinValueValidator

class Recipe(models.Model):
    """Model for storing recipes"""
    
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(help_text="List ingredients line by line")
    instructions = models.TextField(help_text="Cooking instructions step by step")
    
    # Nutritional information
    calories = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    protein = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    carbs = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    fat = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    
    # Additional fields
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at', 'name']
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        """Return string representation of recipe"""
        return f"{self.name} - {self.get_category_display()} ({self.calories} cal)"
    
    @property
    def total_time(self):
        """Calculate total time (preparation + cooking)"""
        return self.preparation_time + self.cooking_time