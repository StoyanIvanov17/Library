from django.contrib import admin

from library.lb_events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'date', 'time', 'location', 'description', 'age_group')
    list_filter = ('date', )
    search_fields = ('name', 'location', 'time')
