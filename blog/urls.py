from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blogsView, name='blog'),
    path('<int:pk>/', views.blogDetailView, name='post_detail'),
    path('new/', views.newBlogView, name='new_blog'),
]
