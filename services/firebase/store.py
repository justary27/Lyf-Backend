from django.core.files.uploadedfile import InMemoryUploadedFile

from globals.variables import firebase_instance
from services.compress.compressors import Compressors


class FirebaseStore:
    storage_instance = firebase_instance.storage()

    @staticmethod
    def upload_file(file_path: str, compressed_image: InMemoryUploadedFile):
        FirebaseStore.storage_instance.child(
            file_path
        ).put(compressed_image.file)

    @staticmethod
    def get_download_url(file_path) -> str:
        return FirebaseStore.storage_instance.child(
            file_path
        ).get_url(None)

    @staticmethod
    def upload_and_get_download_url(file_path: str, image):
        image = Compressors.compress_image(image)
        FirebaseStore.upload_file(file_path, image)

        return FirebaseStore.get_download_url(file_path)
