from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from library.lb_home.forms import BestAuthorsCreateForm
from library.lb_home.models import BestAuthors


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['bestselling_authors'] = BestAuthors.objects.all()
        return context


class CreateBestAuthorsView(views.CreateView):
    model = BestAuthors
    form_class = BestAuthorsCreateForm
    template_name = 'home/create_bestselling_author.html'
    success_url = reverse_lazy('home page')
