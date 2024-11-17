import uuid
from django.contrib.auth import mixins as auth_mixin


from asgiref.sync import sync_to_async
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout, get_user_model

from library.lb_accounts.forms import LibraryUserCreationForm, LibraryProfileForm
from library.lb_accounts.models import LibraryProfile
from library.lb_accounts.utils.library_card_number_generator import generate_library_card_number

UserModel = get_user_model()


class SignInUserView(auth_views.LoginView):
    template_name = 'accounts/account_signin_user.html'
    redirect_authenticated_user = True

    def get_success_url(self):

        user = self.request.user
        if user.is_authenticated and hasattr(user, 'libraryprofile'):
            return reverse("account details", kwargs={"pk": user.libraryprofile.pk})

        return super().get_success_url()


class SignUpUserView(views.CreateView):
    template_name = 'accounts/account_signup_user.html'
    form_class = LibraryUserCreationForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.library_card_number = generate_library_card_number()
        user.is_active = False

        user.save()

        profile = LibraryProfile.objects.create(
            user=user,
            email=user.email,
            verification_token=uuid.uuid4(),
        )

        profile.save()

        verification_url = self.request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': str(profile.verification_token)}))
        send_mail(
            subject="Welcome to the Library!",
            message=f"Please verify your email by clicking the following link: {verification_url}",
            from_email="freakyjackals@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return render(self.request, 'accounts/account_user_confirmation.html')

    def get_success_url(self):
        return self.success_url


class VerifyEmailView(views.View):
    async def get(self, request, token):
        profile = await sync_to_async(LibraryProfile.objects.get)(verification_token=token)

        user = await sync_to_async(UserModel.objects.get)(libraryprofile=profile)
        user.is_active = True
        await sync_to_async(user.save)()

        profile.verified = True
        await sync_to_async(profile.save)()

        await sync_to_async(login)(request, user)

        return redirect('registration profile')


class LibraryProfileCreateView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    model = LibraryProfile
    form_class = LibraryProfileForm
    template_name = 'accounts/account_profile_registration.html'
    success_url = reverse_lazy('account details')

    def get_success_url(self):
        return reverse_lazy('account details', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        profile, created = LibraryProfile.objects.get_or_create(user=self.request.user)
        return profile


def signout_user(request):
    logout(request)
    return redirect('home page')


class AccountDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    queryset = LibraryProfile.objects.all()
    template_name = 'accounts/account_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['saved_items'] = profile.saved_items.all()
        context['saved_events'] = profile.saved_events.all()
        return context


class AccountUpdateView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    queryset = LibraryProfile.objects.all()
    template_name = 'accounts/account_update.html'
    form_class = LibraryProfileForm

    def get_success_url(self):
        return reverse("account details", kwargs={
            "pk": self.object.pk,
        })


class AccountDeleteView(views.DeleteView):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return redirect(reverse_lazy('home page'))
