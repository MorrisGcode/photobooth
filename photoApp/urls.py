from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/profile/', views.home, name="home"),
    path('photo_list/', views.photo_list, name="photo_list"),
    path('photo_detail/<int:photo_id>/', views.photo_detail, name="photo_detail"),
    path('photo_delete/<int:photo_id>/', views.photo_delete, name="photo_delete"),
    path('photo_upload/', views.photo_upload, name="photo_upload"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('like_photo/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('comment_photo/<int:photo_id>/', views.comment_photo, name='comment_photo'),
]