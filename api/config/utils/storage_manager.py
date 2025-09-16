from django.conf import settings
import boto3
from botocore.client import Config
import base64
import io


class CloudStorageManager:
    def __init__(self, region="nyc3"):
        self.access_key = settings.STORAGE_ACCESS_KEY
        self.secret_key = settings.STORAGE_SECRET_KEY
        self.endpoint_url = settings.STORAGE_END_POINT_URL
        self.cdn_url = getattr(settings, "STORAGE_END_POINT_CDN_URL", "")
        self.region = region

        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name=self.region,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4')
        )

    def upload_file(
        self,
        file,
        bucket="images",
        file_key="nested/test_img.svg",
        acl="private",
        is_from_client=False,
    ):
        """Upload file to storage. `acl` can be 'public-read' or 'private'."""
        try:
            if is_from_client:
                self.client.upload_fileobj(
                    Fileobj=file,
                    Bucket=bucket,
                    Key=file_key,
                    ExtraArgs={'ACL': acl}
                )
            else:
                self.client.upload_file(
                    Filename=file,
                    Bucket=bucket,
                    Key=file_key,
                    ExtraArgs={'ACL': acl}
                )
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False

    def get_url(self, bucket="images", file_key="nested/test_img.svg", acl="private"):
        """Get either a signed URL or a public CDN URL based on ACL."""
        try:
            if acl == "private":
                return self._get_signed_url(bucket, file_key)
            elif acl == "public-read" and self.cdn_url:
                return f"{self.cdn_url}/{file_key}"
            else:
                return self._get_signed_url(bucket, file_key)
        except Exception as e:
            print(f"Get URL error: {e}")
            return ""

    def delete_file(self, bucket="images", file_key="nested/test_img.svg"):
        """Delete a file from storage."""
        try:
            self.client.delete_object(
                Bucket=bucket,
                Key=file_key
            )
            print(f"File '{file_key}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def upload_base64(self, data, bucket="images", file_key="nested/test.wav", acl="private"):
        try:
            if isinstance(data, (bytes, bytearray)):
                file_bytes = data

            else:
                base64_data = str(data).strip()
                if "," in base64_data:
                    base64_data = base64_data.split(",")[1]
                file_bytes = base64.b64decode(base64_data)

            file_obj = io.BytesIO(file_bytes)
            self.client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=bucket,
                Key=file_key,
                ExtraArgs={'ACL': acl}
            )
            return file_key
        except Exception as e:
            print(f"Base64 upload error: {e}")
            return None
    
    # ------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------
    
    def _get_signed_url(self, bucket="images", file_key="nested/test_img.svg", expires_in=3600):
        """Generate a signed URL for a private object."""
        try:
            return self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': file_key},
                ExpiresIn=expires_in
            )
        except Exception as e:
            print(f"Signed URL error: {e}")
            return ""