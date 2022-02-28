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
    path('data/', views.data2, name='data2'),
    path('instruments/', views.instruments, name='instruments'),
    # INSTRUMENTS
    path('station/', views.station, name='station'),
    path('intranet/', views.intranet, name='intranet'),
    path('contact/', views.contact, name='contact'),
    path('Air_quality_monitor/', views.Air_quality_monitor, name='Air_quality_monitor'),
    path('APS/', views.APS, name='APS'),
    path('Control_room/', views.Control_room, name='Control_room'),
    path('CPC/', views.CPC, name='CPC'),
    path('Gilibrator/', views.Gilibrator, name='Gilibrator'),
    path('HT_Sensor/', views.HT_Sensor, name='HT_Sensor'),
    path('Inlet_system/', views.Inlet_system, name='Inlet_system'),
    path('Meteo_Station/', views.Meteo_Station, name='Meteo_Station'),
    path('Nephelometer/', views.Nephelometer, name='Nephelometer'),
    path('PM10_PM1/', views.PM10_PM1, name='PM10_PM1'),
    path('PSAP/', views.PSAP, name='PSAP'),
    path('Rack/', views.Rack, name='Rack'),
    path('uRADmonitor/', views.uRADmonitor, name='uRADmonitor'),
    # END INSTRUMENTS


    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)