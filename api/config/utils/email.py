from django.core.mail import BadHeaderError
from django.conf import settings
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, Asm, Category

FROM_EMAIL = "info@iswad.tech"

def _resolve_recipient(email):
    if bool(int(settings.USE_REAL_EMAIL_ADDRESSES)):
        return [email]
    return [email] if email in settings.EMAIL_ADDRESSES_FOR_TESTING else [settings.RECEIVER_EMAIL_FOR_TEST]


def send_email(email, params, email_template_id):
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=_resolve_recipient(email),
        )
        message.dynamic_template_data = params
        message.template_id = email_template_id   
        return settings.SG_SMTP.send(message)
    except BadHeaderError as e:
        print(e)
    except Exception as e:
        print(f"Error sending email: {e}")
    return

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------


def send_email_with_attachment(email, params, attached_file_info, email_template_id, email_template_name):
    """
    attached_file_info = {"file": encoded_pdf, "name": "receipt.pdf", "file_type": "application/pdf"}
    """
    try:
        attachment = Attachment()
        attachment.file_content = FileContent(
            attached_file_info["file"])
        attachment.file_type = FileType(
            attached_file_info["file_type"])
        attachment.file_name = FileName(attached_file_info["name"])
        attachment.disposition = Disposition('attachment')
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=_resolve_recipient(email),
        )
        message.dynamic_template_data = params
        message.template_id = email_template_id
        message.attachment = attachment
        return settings.SG_SMTP.send(message)
    except BadHeaderError as e:
        print(e)
    except Exception as e:
        print(f"Error sending email: {e}")
    return