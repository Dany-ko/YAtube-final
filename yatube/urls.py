from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

from posts import views as view


handler404 = 'posts.views.page_not_found'  # noqa
handler500 = 'posts.views.server_error'  # noqa


urlpatterns = [
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('misc/404/', view.page_not_found, name='page_not_found'),
    path('misc/500/', view.server_error, name='server_error'),
    path('', include('posts.urls')),
]


urlpatterns += [
    path('terms/', views.flatpage,
        {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage,
        {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage,
        {'url': '/about-spec/'}, name='about-spec'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
