from django.urls import path,include
from shop import views
from review import views as review_views
from user import views as user_views
from forsale import views as views3
from feedback import views as feedback_views
from notification import views as notification_views

from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/',user_views.register_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('pos/<int:pk>/',views.pos_detail_view),
    path('pos/<int:pk>/update/',views.pos_update_view),
    path('pos/<int:pk>/delete/',views.pos_delete_view),
    path('pos/create/',views.pos_create_view),
    path('filter-products/', views.filter_products, name='filter_products'),
    path('search/',views.search),
    path('user/details/',user_views.user_details),
    path('shops/',views.shop_create_view),
    path('shop/<int:pk>/',views.shop_view),
    path('shop/<int:pk>/products/',views.shop_products),
    path('user-shops/',views.user_shops_view, name='user-shops'),
    path('fetch_all_pos/',views.fetch_all_pos),
    path('forsale/',views3.forsaleProduct),
    path('forsale2/',views3.fetch_all_forsale),
    path('forsale_details/<int:pk>/',views3.for_sale_detail),
    path('forsale/<int:pk>/update/',views3.forsale_update),
    path('forsale/<int:pk>/delete/',views3.forsale_delete), 
    path('feedback/',feedback_views.get_feedback),
    path('shops/<int:pk>/follow/', views.follow_unfollow_shop, name='follow-unfollow-shop'),
    path("product/<int:product_id>/toggle-save/", user_views.toggle_save_product, name="toggle-save-product"),
    path('saved-products/', user_views.get_saved_products),
    path('reviews/<int:product_id>/',review_views.prod_reviews , name='review-list-create'),
    path('reviews/<int:product_id>/review-summary/', review_views.review_summary, name='review-summary'),
    path('reviews/check/<int:product_id>/', review_views.check_review, name='review-check'),
    path('reviews/update/<int:review_id>/', review_views.update_review, name='update-review'),
    path('reviews/<int:pk>/delete/', review_views.delete_review, name='delete-review'),
    path('user/details/<int:pk>/',user_views.get_other_user_details),
    path('notifications/',notification_views.my_notifications),
    path('notifications/mark-all-as-read/', notification_views.mark_all_notifications_as_read, name='mark-all-notifications-read'),
    path('change-password/', user_views.ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/', user_views.UserProfileUpdateView.as_view()),
    path('product/<int:product_id>/increment-view/', views.IncrementViewCountAPIView.as_view(), name='increment-view'),
    path('product/<int:pk>/recommendations/', views.ProductRecommendationAPIView.as_view(), name='product-recommendations'),
]
