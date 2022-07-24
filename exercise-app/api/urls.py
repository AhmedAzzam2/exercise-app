from django.urls import path
from .views import (
    post_all,
    post_list,
    userpost,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('post_all/<int:pk>/', post_all, name='post_all-api'),
    path('user/<str:username>', userpost, name='user-Posts-api'),
    path('', post_list, name='blog-home-api'),
    # path('user/<str:username>', UserPostListView.as_view-api(), name='user-Posts-api'),
    path('Post/<int:pk>/', PostDetailView.as_view(), name='Post-detail-api'),
    path('Post/new/', PostCreateView.as_view(), name='Post-create-api'),
    path('Post/<int:pk>/update/', PostUpdateView.as_view(), name='Post-update-api'),
    path('Post/<int:pk>/delete/', PostDeleteView.as_view(), name='Post-delete-api'),
    path('media/Files/<int:pk>',PostDeleteView.as_view(),name='Post-delete-api' ),
    path('search/',views.search,name='search-api'),
    path('about/', views.about, name='blog-about-api'),
]
