from django.db import models

from library.core.validators import MaxFileSizeValidator


class BestAuthors(models.Model):
    MAX_NAME_LENGTH = 50

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )

    author_image = models.ImageField(
        upload_to='author_images/',
        blank=False,
        null=False,
        validators=[MaxFileSizeValidator(10 * 1024 * 1024)],
        verbose_name='Author Image'
    )

    def __str__(self):
        return self.name
