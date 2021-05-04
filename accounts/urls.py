# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# Local apps
from accounts import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='accounts_login'),
    path('logout/', LogoutView.as_view(next_page='post_home_page'), name='accounts_logout'),
    path('signup/', views.user_form, name='accounts_signup'),
    path('user-update/<int:id>/', views.user_form, name='accounts_user_update'),
]
