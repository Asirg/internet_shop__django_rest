from django.urls import include, path

from rest_framework.urlpatterns import format_suffix_patterns

from shop import views
from shop import api

urlpatterns = [

]

urlpatterns += format_suffix_patterns([
    path("product/", views.ProductViewSet.as_view({"get": "list"})),
    path("product/<int:pk>/", views.ProductViewSet.as_view({"get": "retrieve"})),
    path("review/", views.ReviewCreateViewSet.as_view({"post": "create"})),
    path("comments/", views.CommentViewSet.as_view({"get": "list"})),
    path("comment/", views.CommentViewSet.as_view({"post": "create"})),
    path("comment/<int:pk>/", views.CommentViewSet.as_view({"put": "update"})),
    path("category/", api.ProductCategoryViewSet.as_view({"get": 'list'})),
    path("category/<slug:url>/", api.ProductCategoryViewSet.as_view({"get": 'retrieve'}))
    ]
)

# urlpatterns = [
#     path("product/", views.ProductListView.as_view()),
#     path("product/<int:pk>/", views.ProductDetailView.as_view()),
#     path("review/", views.ReviewCreateView.as_view()),
#     path("comment/", views.CommentCreateView.as_view()),
#     path("categories/", views.ProductCategoryListView.as_view()),
#     path("categories/<int:pk>/", views.ProductCategoryDetailView.as_view()),
# ]
