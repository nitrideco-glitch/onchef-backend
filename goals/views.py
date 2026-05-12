from rest_framework import generics, permissions
from .models import Goal
from .serializers import GoalSerializer
from users.permissions import IsOwnerOrReadOnly

class GoalListCreateView(generics.ListCreateAPIView):
    """List all goals for current user or create new goal"""
    
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only goals belonging to the current user"""
        user = self.request.user
        queryset = Goal.objects.filter(user=user)
        
        # Optional filtering by goal type
        goal_type = self.request.query_params.get('goal_type')
        if goal_type:
            queryset = queryset.filter(goal_type=goal_type)
        
        # Optional filtering by active goals (not completed)
        active_only = self.request.query_params.get('active_only')
        if active_only and active_only.lower() == 'true':
            queryset = queryset.filter(success_rate__lt=100)
        
        return queryset
    
    def perform_create(self, serializer):
        """Save the goal with the current user"""
        serializer.save(user=self.request.user)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific goal"""
    
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Ensure users can only access their own goals"""
        return Goal.objects.filter(user=self.request.user)