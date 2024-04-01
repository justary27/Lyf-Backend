import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile


class Compressors:

    @staticmethod
    def compress_image(image:UploadedFile):
        with BytesIO(image.file.read()) as buffer:
            img = Image.open(buffer)

            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)

            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{image.name.split('.')[0]}_compressed.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
