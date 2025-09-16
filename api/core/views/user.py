from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings
from rest_framework import views, permissions, response, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
import requests
import json

from core.models import UserModel
from core.serializers import UserSerializer
from core.tasks import send_activation_email_after_register_task, send_reset_password_email_task
from config.utils.tokens import TenMinutesAccessToken, OneDayRefreshToken, ThirtyDaysRefreshToken


class UserViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        try:
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")
            password = request.data.get("password")
            redirect_url = request.data.get("redirect_url", "")
            if not first_name or not last_name or not email or not password:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "First name, last name, email, and password are required."})
            does_email_exist = UserModel.objects.filter(email=email).exists()
            if does_email_exist:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Email already exists."})
            new_user = UserModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=False
            )
            new_user.set_password(password)
            new_user.save()
            client_group = Group.objects.get(name='CLIENT')
            new_user.groups.add(client_group)
            send_activation_email_after_register_task.delay(new_user.id, redirect_url)
            serializer = UserSerializer(new_user)
            return response.Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})

class UserActivateAccountViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, format=None):
        try:
            token_str = request.data.get("token")
            if not token_str:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Token is required."})
            token = AccessToken(token_str)
            user_id = token.get("user_id")
            if not user_id:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found."})
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found."})
            user.is_active = True
            user.register_token = None
            user.save(update_fields=["is_active", "register_token"])
            access_token = str(TenMinutesAccessToken.for_user(user))
            refresh_token = str(OneDayRefreshToken.for_user(user))
            serializer = UserSerializer(user)
            return response.Response(status=status.HTTP_200_OK, data={"user": serializer.data, "access_token": access_token, "refresh_token": refresh_token})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})


class RefreshUserAccessTokenViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            refresh_token_str = request.data.get("refresh_token")
            if not refresh_token_str:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Refresh token is required."})
            refresh_token = RefreshToken(refresh_token_str)
            user_id = refresh_token.get("user_id")
            if not user_id:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found."})
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found."})
            access_token = str(TenMinutesAccessToken.for_user(user))
            return response.Response(status=status.HTTP_200_OK, data={"access_token": access_token})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})


class UserForgotPasswordViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data.get("email")
            if not email:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Email is required."})
            user = UserModel.objects.get(email=email)
            if not user:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found."})
            if user.last_tokenized_email_sent:
                time_since_last_email = timezone.now() - user.last_tokenized_email_sent
                if time_since_last_email < timedelta(hours=24):
                    return response.Response(
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                        data={"message": "Validation email already sent within the last 24 hours."}
                    )
            send_reset_password_email_task.delay(user.id)
            return response.Response(status=status.HTTP_200_OK, data={"success": True})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})
        
class UserResetPasswordViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            token_str = request.data.get("token")
            email = request.data.get("email")
            password = request.data.get("password")
            if not token_str or not email or not password:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Token, email and password are required."})
            token = AccessToken(token_str)
            user_id = token.get("user_id")
            if not user_id:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Token is invalid or expired."})
            user = UserModel.objects.get(email=email)
            if not user:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "No user found with this email address."})
            if user_id != user.id:
                return response.Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Token does not match the user."})
            user.set_password(password)
            user.register_token = None
            user.is_active = True
            user.save(update_fields=["password", "register_token", "is_active"])
            return response.Response(status=status.HTTP_200_OK, data={"success": True})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})

class UserLoginViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            remember_me = request.data.get("remember_me", False)
            if not email or not password:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Email and password are required."})
            user = UserModel.objects.get(email=email)
            if not user:
                return response.Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found with this email address."})
            if not user.is_active:
                return response.Response(status=status.HTTP_403_FORBIDDEN, data={"message": "User account is not active."})
            if not user.check_password(password):
                return response.Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Invalid email/password."})
            access_token = None
            refresh_token = None
            if not remember_me:
                access_token = str(TenMinutesAccessToken.for_user(user))
                refresh_token = str(OneDayRefreshToken.for_user(user))
            else:
                access_token = str(TenMinutesAccessToken.for_user(user))
                refresh_token = str(ThirtyDaysRefreshToken.for_user(user))
            serializer = UserSerializer(user)
            return response.Response(status=status.HTTP_200_OK, data={"user": serializer.data, "access_token": access_token, "refresh_token": refresh_token})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})

class UserLogOutViewSet(views.APIView):

    def post(self, request, format=None):
        try:
            refresh_token_str = request.data.get("refresh_token", "")
            if not refresh_token_str:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "message": "Refresh token is required."})
            RefreshToken(refresh_token_str).blacklist()
            return response.Response(status=status.HTTP_200_OK, data={"success": True})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"success:": False, "message": f"{str(e)}"})
        










class UserAuthWithGoogleViewSet(views.APIView):

    def post(self, request, *args, **kwargs):
        try:
            client_id = settings.GOOGLE_AUTH_CLIENT_ID
            client_secret = settings.GOOGLE_AUTH_CLIENT_SECRET
            ouathUrl = "https://oauth2.googleapis.com/token"
            redirect_url = f"{settings.CLIENT_URL}/app/google-auth/"
            code = request.data.get("code")
            if not code:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Code is required."})
            googleTokenReqApiUrl = f"{ouathUrl}?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_url}&grant_type=authorization_code&code={code}"  
            res = requests.post(googleTokenReqApiUrl)
            return response.Response(status=status.HTTP_200_OK, data=json.loads(res.content))
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": str(e)})


class UserLoginWithGoogleViewSet(views.APIView):

    def post(self, request, *args, **kwargs):
        try:
            id_token = request.data.get("id_token")
            access_token = request.data.get("access_token")
            if not id_token or not access_token:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "id_token and access_token are required."})
            googleAuthGetProfileUrl = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            headers = {"Content-Type": "application/json",
                "Authorization": access_token}
            res = requests.get(googleAuthGetProfileUrl, headers=headers)
            user_data = json.loads(res.content)
            email = user_data.get("email")
            if not email:
                return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Email not found in Google profile."})
            user = UserModel.objects.filter(email=email).first()
            if not user:
                first_name = user_data.get("given_name")
                last_name = user_data.get("family_name")
                if not first_name and not last_name:
                    first_name = user_data.get("name")
                user = UserModel(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=True
                )
                user.save()
                client_group = Group.objects.get(name='CLIENT')
                user.groups.add(client_group)
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            access_token = str(TenMinutesAccessToken.for_user(user))
            refresh_token = str(OneDayRefreshToken.for_user(user))
            serializer = UserSerializer(user)
            return response.Response(status=status.HTTP_200_OK, data={"user": serializer.data, "access_token": access_token, "refresh_token": refresh_token})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": str(e)})