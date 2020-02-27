from django.urls import path, include
from .views import registerView, MyLoginView, profileView

app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', registerView, name='register'),
    path('profile/<int:pk>/', profileView, name='profile'),
]