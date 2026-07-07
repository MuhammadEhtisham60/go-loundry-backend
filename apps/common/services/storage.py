import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class StorageService:
    """
    Abstraction layer for handling file uploads.
    Facilitates easy swapping between local storage, AWS S3, and Firebase Storage.
    """

    @staticmethod
    def upload_file(file_obj, folder: str = "uploads") -> str:
        """
        Uploads a file and returns its public URL.
        By default, uses Django's local storage and simulates a public URL.
        """
        filename = f"{folder}/{file_obj.name}"
        path = default_storage.save(filename, ContentFile(file_obj.read()))
        # In a real environment, this would return the S3/Firebase public url
        # For our development placeholder, return local server URL format
        return f"/media/{path}"
