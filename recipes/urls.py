from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeByCategoryView

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe-list'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('category/<str:category>/', RecipeByCategoryView.as_view(), name='recipe-by-category'),
]