from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserViewSet),
    path('user-activate-account/', views.UserActivateAccountViewSet),
    path('refresh-user-access-token/', views.RefreshUserAccessTokenViewSet),
    path('user-forgot-password/', views.UserForgotPasswordViewSet),
    path('user-reset-password/', views.UserResetPasswordViewSet),
    path('user-login/', views.UserLoginViewSet),
    path('user-logout/', views.UserLogOutViewSet),
    path('user-auth-with-google/', views.UserAuthWithGoogleViewSet),
    path('user-login-with-google/', views.UserLoginWithGoogleViewSet),

    path('profile/', views.ProfileViewSet)
]
