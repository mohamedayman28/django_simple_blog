# Django
from django.shortcuts import reverse
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    # Redirect to post_list view.
    redirect_authenticated_user = True

    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse('post_list')
