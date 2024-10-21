from django.contrib import admin

from library.lb_collections.models import Item, Review


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author__name', 'genre', 'item_type', 'publication_date', 'isbn')
    search_fields = ['title', 'author__name', 'genre', 'item_type']
    ordering = ['pk']


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'item', 'rating', 'comment', 'created_at')
    search_fields = ['user__email', 'item__title']
    ordering = ['-created_at']
    list_filter = ('created_at', )

