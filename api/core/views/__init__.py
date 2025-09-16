from . import user, profile

UserViewSet = user.UserViewSet.as_view()
UserActivateAccountViewSet = user.UserActivateAccountViewSet.as_view()
RefreshUserAccessTokenViewSet = user.RefreshUserAccessTokenViewSet.as_view()
UserForgotPasswordViewSet = user.UserForgotPasswordViewSet.as_view()
UserResetPasswordViewSet = user.UserResetPasswordViewSet.as_view()
UserLoginViewSet = user.UserLoginViewSet.as_view()
UserLogOutViewSet = user.UserLogOutViewSet.as_view()
UserAuthWithGoogleViewSet = user.UserAuthWithGoogleViewSet.as_view()
UserLoginWithGoogleViewSet = user.UserLoginWithGoogleViewSet.as_view()

ProfileViewSet = profile.ProfileViewSet.as_view()