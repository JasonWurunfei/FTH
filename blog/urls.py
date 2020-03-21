from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blogsView, name='blog'),
    path('<int:pk>/', views.blogDetailView, name='post_detail'),
    path('new/', views.newBlogView, name='new_blog'),
    path('new/<int:pk>/', views.editBlogView, name='edit_blog'),

    path('series/', views.seriesView, name='series'),
    path('series/<int:pk>/', views.seriesDetailView, name='series_detail'),
    path('series/new/', views.newSeriesView, name='new_series'),
    path('series/new/<int:pk>/', views.editSeriesView, name='edit_series'),

    # AJAX request
    path('ajax/delete_blog/', views.delete_blog, name='delete_blog'),
    path('ajax/delete_series/', views.delete_series, name='delete_series'),
]
