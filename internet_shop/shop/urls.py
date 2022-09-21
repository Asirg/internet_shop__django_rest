from django.urls import include, path

from shop import views

urlpatterns = [
    path("product/", views.ProductListView.as_view()),
    path("product/<int:pk>/", views.ProductDetailView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("comment/", views.CommentCreateView.as_view()),
    path("categories/", views.ProductCategoryListView.as_view()),
    path("categories/<int:pk>/", views.ProductCategoryDetailView.as_view()),
]