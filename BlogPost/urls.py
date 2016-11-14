"""BlogPost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', acc_logout, name='logout'),
    url(r'^home/$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^post/(?P<pid>\d*)/$', post, name='post'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^blog/$', blog, name='blog'),
    url(r'^blog/(?P<bid>\d*)/delete/$', blog_remove, name="blog_remove"),
    url(r'^author/$', author, name='author'),
    url(r'^author/(?P<aid>\d*)/delete/$', author_remove, name="author_remove"),
    url(r'^category/$', category, name='category'),
    url(r'^category/(?P<cid>\d*)/delete/$', category_remove, name="category_remove"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
