from django.conf import settings
from datetime import datetime

from config.utils.tokens import OneDayAccessToken
from config.utils.email import send_email
from core.models import UserModel
from core.utils.sg_templates import SG_TEMPLATE_IDS

def send_activation_email_after_register(user_id, redirect_url=""):
    try:
        user = UserModel.objects.filter(id=user_id).first()
        user_token = str(OneDayAccessToken.for_user(user))
        user.register_token = user_token
        user.save(update_fields=["register_token"])
        email_template_id = SG_TEMPLATE_IDS["VERIFY_YOUR_REGISTRATION"]
        params = {}
        params["first_name"] = user.first_name
        params["activate_link"] = f"{settings.CLIENT_URL}/app/activate-user?token={user_token}"
        if redirect_url:
            params["activate_link"] = f"{settings.CLIENT_URL}/app/activate-user?token={user_token}&redirect_url={redirect_url}"
        send_email(user.email, params, email_template_id)
        user.last_tokenized_email_sent = datetime.now()
        user.save(update_fields=["last_tokenized_email_sent"])
        return True
    except Exception as e:
        print(f"Error sending activation email: {str(e)}")
        return False

def send_reset_password_email(user_id):
    try:
        user = UserModel.objects.get(id=user_id)
        if not user:
            return False
        user_token = str(OneDayAccessToken.for_user(user))
        user.register_token = user_token
        user.save(update_fields=["register_token"])
        email_template_id = SG_TEMPLATE_IDS["RESET_PASSWORD"]
        params = {}
        params["first_name"] = user.first_name
        params["reset_link"] = f"{settings.CLIENT_URL}/app/reset-password?token={user_token}&email={user.email}"
        params["expiration_duration"] = "24 hours"
        send_email(user.email, params, email_template_id)
        user.last_tokenized_email_sent = datetime.now()
        user.save(update_fields=["last_tokenized_email_sent"])
        return True
    except Exception as e:
        print(f"Error sending reset password email: {str(e)}")
        return False