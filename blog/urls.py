# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Third party
import debug_toolbar
from filebrowser.sites import site


urlpatterns = [
    # Local Django.
    path('', include('posts.urls')),  # Posts
    path('accounts/', include('accounts.urls')),  # Accounts app.

    # Django
    path('admin/', admin.site.urls),  # Admin

    # Third party
    path('tinymce/', include('tinymce.urls')),  # TinyMCE
    path('admin/filebrowser/', site.urls),  # FileBrowser
]


if settings.DEBUG:
    # Django
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Third party
    urlpatterns += path('__debug__', include(debug_toolbar.urls)),  # Django debug toolbar
