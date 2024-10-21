from django import forms

from library.lb_events.models import Event


class EventBaseForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date', 'time', 'location', 'age_group', 'event_image', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'date': forms.DateInput(attrs={'placeholder': 'Date', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'placeholder': 'Time', 'type': 'time', 'step': '900'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'age_group': forms.TextInput(attrs={'placeholder': 'Age Group'}),
            'event_image': forms.FileInput(attrs={'placeholder': 'Event Image'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }


class EventCreateForm(EventBaseForm):
    pass
