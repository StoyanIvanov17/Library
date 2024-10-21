from django.contrib.auth import mixins as auth_mixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic as views
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.lb_collections.forms import ItemCreateForm, ItemEditForm, ReviewForm
from library.lb_collections.models import Item, Review
from library.utils.save_functionality import toggle_saved_object


class BookCreateView(auth_mixin.LoginRequiredMixin, views.CreateView):
    queryset = Item.objects.all()
    form_class = ItemCreateForm
    template_name = 'collections/item_create.html'
    success_url = reverse_lazy('item display')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.instance.user = self.request.user

        return form


class ItemListView(views.ListView):
    template_name = 'collections/item_display.html'

    def filter_by_genre(self, queryset):
        genre_query = self.request.GET.get('genre', '')
        item_type_query = self.request.GET.get('item_type', '')

        query = Q()

        if genre_query:
            query &= Q(genre__icontains=genre_query)

        if item_type_query and item_type_query != 'All':
            query &= Q(item_type=item_type_query)

        return queryset.filter(query)

    def get_queryset(self):
        queryset = Item.objects.all()
        return self.filter_by_genre(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_query'] = self.request.GET.get('genre', '')
        context['item_type_query'] = self.request.GET.get('item_type', '')
        context['item_choices'] = Item.ItemTypeChoices.choices
        context['items'] = self.get_queryset()

        return context


class ItemDetailView(views.DetailView):
    queryset = Item.objects.all()
    template_name = 'collections/item_detail.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = self.form_class()
        context['reviews'] = Review.objects.filter(item=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            form = self.form_class(request.POST)

            if form.is_valid():
                review = form.save(commit=False)
                review.item = item
                review.user = request.user
                review.save()

                return JsonResponse({
                    'success': True,
                    'review_text': review.comment,
                    'username': request.user.libraryprofile.full_name,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })

            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)


class ItemEditView(views.UpdateView):
    queryset = Item.objects.all()
    template_name = 'collections/item_update.html'
    form_class = ItemEditForm
    success_url = reverse_lazy('item display')


class ItemDeleteView(views.DeleteView):
    queryset = Item.objects.all()
    success_url = reverse_lazy('item display')


class SaveItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, slug):
        try:
            user_profile = request.user.libraryprofile
            favorited = toggle_saved_object(user_profile, Item, 'saved_items', pk)

            return Response({'favorited': favorited}, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
            return Response({'success': False, 'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
