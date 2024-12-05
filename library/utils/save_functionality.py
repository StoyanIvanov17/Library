from django.shortcuts import get_object_or_404


def toggle_saved_object(user_profile, model, saved_field_name, pk):
    """
    Toggle the saved status of an object (item/event) for a user.

    :param user_profile: The user's profile (LibraryProfile)
    :param model: The model class (e.g., Item or Event)
    :param saved_field_name: The name of the field for saving (e.g., 'saved_items' or 'saved_events')
    :param pk: The primary key of the object to save/remove
    :return: Boolean indicating whether the object is now saved (True) or unsaved (False)
    """
    obj = get_object_or_404(model, pk=pk)
    saved_field = getattr(user_profile, saved_field_name)

    if obj in saved_field.all():
        saved_field.remove(obj)
        favorited = False
    else:
        saved_field.add(obj)
        favorited = True

    return favorited
