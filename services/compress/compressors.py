import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Compressors:

    @staticmethod
    def compress_image(image):
        img = Image.open(image)
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            'ImageField',
            f"{image.name.split('.')[0]}_compressed.jpg",
            'image/jpeg',
            sys.getsizeof(output),
            None
        )