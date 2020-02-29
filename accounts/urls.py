from django.urls import path, include
from .views import registerView, MyLoginView, profileView, validate_username, validate_email, delet_blog

app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>/', profileView, name='profile'),
    path('register/', registerView, name='register'),
    path('ajax/validate_username/', validate_username, name='validate_username'),
    path('ajax/validate_email/', validate_email, name='validate_email'),
    path('ajax/delet_blog/', delet_blog, name='delet_blog'),
]