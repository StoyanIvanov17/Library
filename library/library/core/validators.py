from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxFileSizeValidator(BaseValidator):
    message = 'Ensure this file size is not greater than %(limit_value)s. Your file size is %(show_value)s.'
    code = 'file_size_limit'

    def clean(self, file):
        return file.size

    def compare(self, file_size, max_size):
        return file_size > max_size
