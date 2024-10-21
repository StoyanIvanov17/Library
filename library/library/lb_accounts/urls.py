from django.urls import path, include

from library.lb_accounts import views
from library.lb_accounts.views import VerifyEmailView

urlpatterns = [
    path('signin/', views.SignInUserView.as_view(), name='signin user'),
    path('signup/', views.SignUpUserView.as_view(), name='signup user'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('signout/', views.signout_user, name='signout user'),
    path('register-profile/', views.LibraryProfileCreateView.as_view(), name='registration profile'),
    path('myaccount/<int:pk>/', include([
        path('', views.AccountDetailsView.as_view(), name='account details'),
        path('edit/', views.AccountUpdateView.as_view(), name='account edit'),
    ]))
]
