def get_media_upload_path(instance, filename):
    folder = instance.post_type.lower()
    return f"{folder}/{filename}"
