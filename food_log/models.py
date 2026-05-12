from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class FoodLog(models.Model):
    """Model for logging food entries"""
    
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_logs'
    )
    food_name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, default='snack')
    
    # Nutritional information
    calories = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    protein = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    carbs = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    fat = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0)])
    
    # Timestamps
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Logs'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['meal_type']),
        ]
    
    def __str__(self):
        """Return string representation of food log"""
        return f"{self.user.email} - {self.food_name} - {self.date}"
    
    @property
    def total_nutrients(self):
        """Calculate total nutrients (for potential extensions)"""
        return {
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
        }