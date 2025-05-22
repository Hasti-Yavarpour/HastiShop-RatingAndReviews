from django.urls import path
from . import views

app_name = "shop"  # ✅ Register the namespace!

urlpatterns = [
    path('', views.shop_home, name='shop_home'),  # http://127.0.0.1:8001/shop/
    path('products/', views.product_list, name='product_list'),

    # ⭐ Rating API endpoints:
    path('api/products/<int:product_id>/reviews/submit/', views.submit_review, name='submit_review'),
    path('api/products/<int:product_id>/reviews/', views.get_reviews, name='get_reviews'),
    path('api/products/<int:product_id>/average-rating/', views.get_average_rating, name='get_average_rating'),
    path('api/products/<int:product_id>/rating-distribution/', views.get_rating_distribution, name='rating_distribution'),
    path('moderate-reviews/', views.review_moderation, name='review_moderation'),
    path('api/reviews/<int:review_id>/approve/', views.approve_review, name='approve_review'),
    path('api/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]

