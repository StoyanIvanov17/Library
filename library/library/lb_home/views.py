from django.shortcuts import render
from django.views import generic as views


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context
