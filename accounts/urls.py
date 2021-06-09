# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# Local apps
from accounts import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='accounts_login'),
    path('logout/', LogoutView.as_view(next_page='post_list'), name='accounts_logout'),
]
