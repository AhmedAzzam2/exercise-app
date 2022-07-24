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
    path('post_all/<int:pk>/', post_all, name='post_all'),
    path('user/<str:username>', userpost, name='user-Posts'),
    path('', post_list, name='blog-home'),
    # path('user/<str:username>', UserPostListView.as_view(), name='user-Posts'),
    path('Post/<int:pk>/', PostDetailView.as_view(), name='Post-detail'),
    path('Post/new/', PostCreateView.as_view(), name='Post-create'),
    path('Post/<int:pk>/update/', PostUpdateView.as_view(), name='Post-update'),
    path('Post/<int:pk>/delete/', PostDeleteView.as_view(), name='Post-delete'),
    path('media/Files/<int:pk>',PostDeleteView.as_view(),name='Post-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),
]
