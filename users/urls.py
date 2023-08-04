from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    EditUserView,
    EditPasswordView,
    LogoutUsuarioView,
    RegisterUserView,
)


app_name = 'users'


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('edit/', EditUserView.as_view(), name='edit'),
    path('edit-password/', EditPasswordView.as_view(), name='edit-password'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
]
