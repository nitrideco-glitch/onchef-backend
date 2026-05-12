from django.urls import path
from .views import FoodLogListCreateView, FoodLogDetailView

urlpatterns = [
    path('', FoodLogListCreateView.as_view(), name='food-log-list-create'),
    path('<int:pk>/', FoodLogDetailView.as_view(), name='food-log-detail'),
]