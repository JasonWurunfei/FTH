from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('login/', views.MyLoginView.as_view(), name='login'),
    # path('register/', views.registerView, name='register'),
    # path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>/', views.profileView, name='profile'),
    path('profile/<int:pk>/series/', views.profileSeriesView, name='series'),
    path('settings/<int:pk>/', views.profileSettingsView, name='settings'),
    path('settings/<int:pk>/edit/', views.profileSettingsEditView, name='settings_edit'),
    
    # AJAX urls
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_email/', views.validate_email, name='validate_email'),
]