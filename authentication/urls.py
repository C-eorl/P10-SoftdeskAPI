from django.urls import path

from config.urls import urlpatterns

urlpatterns = [
    # Inscription et connexion
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Gestion du profil
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Refresh token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]