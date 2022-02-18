"""wGOA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from wGOA import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('index/', views.index, name='homepage'),
    path('data/', views.data, name='data'),
    path('instruments/', views.instruments, name='instruments'),
    path('station/', views.station, name='station'),
    path('intranet/', views.intranet, name='intranet'),
    path('contact/', views.contact, name='contact'),
    path('instrument1/', views.instrument1, name='instrument1'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
