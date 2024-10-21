from django.db import models
from django.utils.text import slugify

from library.core.validators import MaxFileSizeValidator
from library.lb_accounts.models import LibraryUser


class Event(models.Model):
    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    date = models.DateField()

    time = models.CharField(
        max_length=20,
    )

    location = models.CharField(
        max_length=255
    )

    age_group = models.CharField(
        max_length=50,
        verbose_name='Age Group'
    )

    event_image = models.ImageField(
        upload_to='event_images/',
        blank=False,
        null=False,
        validators=[MaxFileSizeValidator(10 * 1024 * 1024)],
        verbose_name='Event Image',
    )

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        date_str = self.date.strftime('%Y-%B-%d')
        slug_base = f"{self.name}-{date_str}-{self.location}-{self.age_group}"
        self.slug = slugify(slug_base)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
