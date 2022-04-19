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

    path('test/', views.test, name='test'),
    path('demo/', views.demo, name='demo'),

    path('cpc/', views.cpc_det, name='cpc'),
    path('cpcD/', views.Dcpc_det, name='cpcD'),
    path('apsD/', views.Daps_det, name='apsD'),
    path('nephD/', views.Dneph_det, name='nephD'),
    path('psapD/', views.Dpsap_det, name='psapD'),
    path('aps/', views.aps_det, name='aps'),
    path('psap/', views.psap_det, name='psap'),
    path('neph/', views.neph_det, name='neph'),

    # INTRANET
    path('intranet/SOPs/GOA-UVa-Station-SOP/', views.GOAUVa_Station_SOP, name='GOA-UVa-Station-SOP'),
    path('intranet/SOPs/Neph-SOP/', views.Neph_SOP, name='Neph-SOP'),
    path('intranet/SOPs/APS-SOP/', views.APS_SOP, name='Neph-SOP'),
    path('intranet/SOPs/CPC-SOP/', views.CPC_SOP, name='Neph-SOP'),
    path('intranet/SOPs/PSAP-SOP/', views.PSAP_SOP, name='Neph-SOP'),

    path('intranet/Manuals/Gilibrator2/Gilib-2_850190M-H', views.show_Gilib, name='pdf-file'),
    path('intranet/Manuals/VAISALA/HMT330', views.show_HMT330, name='pdf-file'),
    path('intranet/Manuals/HeaterTape-HTWC102-004/HTWC_Series', views.show_HTWC, name='pdf-file'),
    path('intranet/Manuals/HeaterTape-HTWC102-004/M1046', views.show_M1046, name='pdf-file'),

    path('intranet/Manuals/WeatherStation-Oregon-WMR928NX/WMR928NX', views.show_WMR928NX, name='pdf-file'),
    path('intranet/Manuals/Routers-Linksys/MANUAL000000300', views.show_MANUAL000000300, name='pdf-file'),
    path('intranet/Manuals/Antenna/p172401_en', views.show_p172401_en, name='pdf-file'),
    path('intranet/Manuals/Webcam-DLink-DCS910/dcs910', views.show_dcs910, name='pdf-file'),


    path('intranet/Manuals/Electric-Actuator-J2H20/J2H20', views.show_J2H20, name='pdf-file'),
    path('intranet/Manuals/Rotameters/KeyInstruments-MR300/mr-manual', views.show_MR300, name='pdf-file'),
    path('intranet/Manuals/Pumps/Busch/Seco-SV-1003-D', views.show_Seco_SV_1003, name='pdf-file'),
    path('intranet/Manuals/AirConditioner-W09AH/3828A28001B_MANUAL_OWNERS', views.show_3828A28001B_MANUAL_OWNERS, name='pdf-file'),
    path('intranet/Manuals/Air-Extractor-TD160-100-ecowatt/td_ecowatt_fid4578', views.show_td_ecowatt_fid4578, name='pdf-file'),
    path('intranet/Manuals/Electric-Actuator-J3CH20/J3C-Catalogue-WebRev9', views.show_J3C_Catalogue_WebRev9, name='pdf-file'),
    path('intranet/Manuals/Rotameters/Swagelok-GM06MZ-G212M10Z/MS-02-346', views.show_MS_02_346, name='pdf-file'),
    path('intranet/Manuals/Pumps/KNF-N86KN18/KNF003_EN', views.show_KNF003_EN, name='pdf-file'),
    path('intranet/Manuals/Electric-Actuator-J3CH20/MuB_el_Stellantrieb_Serie_J3_J3C_en', views.show_MuB_el_Stellantrieb_Serie_J3_J3C_en, name='pdf-file'),
    path('intranet/Manuals/Rotameters/Tecfluid-2150/2000_esp', views.show_2000_esp, name='pdf-file'),
    path('intranet/Manuals/Electric-Actuator-J3CH20/00000038', views.show_00000038, name='pdf-file'),
    path('intranet/Manuals/Rotameters/Tecfluid-2150/MI_2000_rev2', views.show_MI_2000_rev2, name='pdf-file'),

    # path('intranet/Manuals/', views.show_, name='pdf-file'),
    # path('intranet/Manuals/', views.show_, name='pdf-file'),

    path('intranet/Software/PSAP/PSAPacquire', views.PSAPacquire, name='PSAPacquire'),
    path('intranet/Software/HTsensor/VAISALAacquire', views.VAISALAacquire, name='VAISALAacquire'),
    path('intranet/Software/scripts/rsync-webcam', views.rsync_webcam, name='rsync_webcam'),
    path('intranet/Software/scripts/save-webcam', views.save_webcam, name='save_webcam'),
    path('intranet/Software/scripts/rsync-laptop', views.rsync_laptop, name='rsync_laptop'),
    path('intranet/Software/scripts/rsync-rawData', views.rsync_rawData, name='rsync-rawData'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)