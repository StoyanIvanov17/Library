from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxFileSizeValidator(BaseValidator):

    def clean(self, file):
        return file.size

    def compare(self, file_size, max_size):
        return file_size > max_size
