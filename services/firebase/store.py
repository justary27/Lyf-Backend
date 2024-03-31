from django.core.files.uploadedfile import InMemoryUploadedFile

from globals.variables import firebase_instance
from services.compress.compressors import Compressors


class _FirebaseStore:
    storage_instance = firebase_instance.storage()

    def upload_file(self, file_path: str, compressed_image: InMemoryUploadedFile):
        self.storage_instance.child(
            file_path
        ).put(compressed_image.file)

    def get_download_url(self, file_path) -> str:
        return self.storage_instance.child(
            file_path
        ).get_url()

    def upload_and_get_download_url(self, file_path: str, image):
        image = Compressors.compress_image(image)
        self.upload_file(file_path, image)

        return self.get_download_url(file_path)
