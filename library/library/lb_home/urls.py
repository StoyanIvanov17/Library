from django.urls import path

from library.lb_home import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home page')
]
