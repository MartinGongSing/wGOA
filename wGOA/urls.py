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
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('index/', views.index, name='homepage'),
    path('data/', views.data1, name='data'),
    path('graph/', views.plot, name='graph'),
    path('instruments/', views.instruments, name='instruments'),
    path('instrum_detail/<int:id>/', views.dyna_instrum, name='instrum_detail'),
    path('station/', views.station, name='station'),
    path('intranet/', views.intranet, name='intranet'),
    path('previous/', views.previous, name='previous'),
    path('contact/', views.contact, name='contact'),

    path('webcam_feed', views.webcam_feed, name='webcam_feed'),

    path('data4/', views.data4, name='data4'),
    path('cpc/', views.cpc_det, name='cpc'),
    path('cpcD/', views.Dcpc_det, name='cpc'),
    path('aps/', views.aps_det, name='aps'),
    path('psap/', views.psap_det, name='psap'),
    path('neph/', views.neph_det, name='neph'),


    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)