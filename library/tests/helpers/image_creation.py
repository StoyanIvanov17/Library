import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def create_test_image():
    image = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return SimpleUploadedFile(
        name='test_image.jpg',
        content=img_byte_arr.getvalue(),
        content_type='image/jpeg'
    )