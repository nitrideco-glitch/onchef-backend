from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Goal(models.Model):
    """Model for user goals (weight, nutrition, fitness)"""
    
    GOAL_TYPES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('maintenance', 'Maintenance'),
        ('muscle_gain', 'Muscle Gain'),
        ('nutrition', 'Nutrition Improvement'),
    ]
    
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    
    # Target values
    target_value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    current_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Success tracking
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Date fields
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'goal_type']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        """Return string representation of goal"""
        return f"{self.user.email} - {self.get_goal_type_display()} ({self.period})"
    
    def calculate_success_rate(self):
        """Calculate success rate based on current and target values"""
        if self.current_value and self.target_value > 0:
            if self.goal_type == 'weight_loss':
                # For weight loss, lower current value is better
                rate = ((self.target_value - self.current_value) / self.target_value) * 100
                self.success_rate = max(0, min(100, rate))
            else:
                # For other goals, higher current value is better
                rate = (self.current_value / self.target_value) * 100
                self.success_rate = max(0, min(100, rate))
        else:
            self.success_rate = 0
        
        self.save(update_fields=['success_rate'])
        return self.success_rate
    
    def is_completed(self):
        """Check if goal is completed"""
        return self.success_rate >= 100
    
    def days_remaining(self):
        """Calculate days remaining until end date"""
        today = date.today()
        if self.end_date >= today:
            return (self.end_date - today).days
        return 0