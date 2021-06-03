"""FaraPy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import settings
from blog import views
from blog import models
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin-farapy/', admin.site.urls),path('', views.index, name='home'),
    path('access/', views.access, name='access'),
    path('category/<int:id>/', views.category, name='category'),
    path('post/<str:id>/', views.post, name='post'),
    path('page/<str:id>/', views.page, name='page'),
    path('multi/<int:id>/', views.multi, name='multi'),
    path('search/', views.search, name='search'),
    path('getanswer/<int:id>/', views.getanswer, name='getanswer'),
    path('getmem/', views.getmem, name='getmem'),
    path('getcom/<int:id>/', views.getcom, name='getcom'),
    path('dc/<int:id>/', views.dc, name='dc'),
    path('getanswer/<int:id>/', views.getanswer, name='getanswer'),
    path('install/', views.install),
    path('panel', views.panel),
    path('panel/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',views.login_user,name="login"),
    path('login', views.login_user, name="login"),


    path('manage_tickets/', views.manage_tickets, name="manage_tickets"), # for Faral
    path('manage_subtickets/', views.manage_subtickets, name="manage_subtickets"), # for Faral

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
the = models.Setting.objects.last()
theme = the.theme.name
staticc = str('themes/' + str(theme))

urlpatterns += static(settings.Themes_URL,document_root=staticc)
urlpatterns += static(settings.Themes_URL2,document_root=settings.Themes_Root)
# d# d###
