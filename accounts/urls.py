from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'accounts'
urlpatterns = [
    # path('login/', views.MyLoginView.as_view(), name='login'),
    # path('register/', views.registerView, name='register'),
    # path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>/', views.profileView, name='profile'),
    path('profile/<int:pk>/series/', views.profileSeriesView, name='series'),
    path('settings/', TemplateView.as_view(template_name='registration/profile_settings.html'), name='settings'),
    
    # AJAX urls
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_email/', views.validate_email, name='validate_email'),
]