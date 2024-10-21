from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

from library.core.validators import MaxFileSizeValidator
from library.lb_collections.core.isbn_generator import generate_isbn


UserModel = get_user_model()


class Author(models.Model):
    MAX_NAME_LENGTH = 50

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )

    bio = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    class ItemTypeChoices(models.TextChoices):
        BOOK = 'book', 'Book'
        AUDIOBOOK = 'audiobook', 'Audio Book'
        MAGAZINE = 'magazine', 'Magazine'

    MAX_TITLE_LENGTH = 255
    MAX_ITEM_TYPE_LENGTH = max(len(x) for x in ItemTypeChoices)
    MAX_ISBN_LENGTH = 13

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='items_author'
    )

    genre = models.CharField(
        max_length=100,
    )

    item_type = models.CharField(
        max_length=MAX_ITEM_TYPE_LENGTH,
        choices=ItemTypeChoices.choices
    )

    publication_date = models.DateField()

    isbn = models.CharField(
        max_length=MAX_ISBN_LENGTH,
        unique=True
    )

    sample = models.TextField()

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    item_image = models.ImageField(
        upload_to='item_images/',
        blank=False,
        null=False,
        validators=[MaxFileSizeValidator(10 * 1024 * 1024)],
    )

    def save(self, *args, **kwargs):
        if not self.isbn:
            self.isbn = generate_isbn()
        date_str = self.publication_date.strftime('%Y-%B-%d')
        slug_base = f"{self.item_type}-{date_str}-{self.author}-{self.title}-{self.genre}"
        self.slug = slugify(slug_base)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
