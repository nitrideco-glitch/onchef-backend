from rest_framework import generics, permissions
from .models import FoodLog
from .serializers import FoodLogSerializer
from users.permissions import IsOwnerOrReadOnly

class FoodLogListCreateView(generics.ListCreateAPIView):
    """List all food logs for current user or create new food log"""
    
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only food logs belonging to the current user"""
        user = self.request.user
        queryset = FoodLog.objects.filter(user=user)
        
        # Optional filtering by date
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)

        return queryset
        
        # Optional filtering by meal type
        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        return queryset
    
    def perform_create(self, serializer):
        """Save the food log with the current user"""
        serializer.save(user=self.request.user)

class FoodLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific food log"""
    
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Ensure users can only access their own food logs"""
        return FoodLog.objects.filter(user=self.request.user)