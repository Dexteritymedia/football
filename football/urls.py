"""
URL configuration for football project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap, index

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
#from wagtail.contrib.sitemaps.views import sitemap
from wagtail.contrib.sitemaps import views as sitemaps_views
from wagtail.contrib.sitemaps import Sitemap

from app.sitemaps import TeamSitemap, TeamListSitemap, StaticSitemap

import environ
from allauth.account.views import LoginView, SignupView

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
ADMIN_URL = env('ADMIN_URL')
BLOG_ADMIN_URL = env('BLOG_ADMIN_URL')


sitemaps = {
    'team-analysis': TeamSitemap,
    'static': StaticSitemap,
    'teams': TeamListSitemap,
}
list_sitemaps = {
    'teams': TeamListSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('', include('app.urls')),
    path('words-building/', include('anagram.urls')),

    path(
        "sports-sitemap.xml/",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    #submitted sitemap to google
    path('sitemap-list.xml/', index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    # sitemap-<section>.xml here <section> will be replaced by the key from sitemaps dict
    path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('list-sitemap.xml/', sitemap, {'sitemaps': list_sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    
    #path('sitemap.xml', sitemap),
    #re_path(r'^sitemap\.xml$', sitemaps_views.sitemap),
    
    path('sitemap-index.xml/', sitemaps_views.index, {
        'sitemaps': {
            'pages': Sitemap
        },
        'sitemap_url_name': 'sitemap',
    }),

    #wagtail sitemap
    re_path(r'^blog-sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    #path('sitemap-pages.xml/', sitemaps_views.sitemap, name='sitemap'),



    path(f'{BLOG_ADMIN_URL}/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('blog/', include(wagtail_urls)),

    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'blog/images/favicon.ico'))
    ]
