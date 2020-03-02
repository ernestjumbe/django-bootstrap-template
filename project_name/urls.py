from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    # Examples:
    # re_path(r'^$', 'mysite.views.home', name='home'),
    # re_path(r'^blog/', blog.urls),
    re_path(r'^$', TemplateView.as_view(template_name="index.html"), {}, name='index'),

    path('admin', admin.site.urls),
]

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
