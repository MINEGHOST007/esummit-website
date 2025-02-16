from django.urls import path
from qr.views import *

app_name = 'qr'
urlpatterns = [
    path('', home, name='home'),
    path('profile', profile, name="profile"),
    path('scanner', scanner, name="scanner"),
    # # path('scan/', scan, name='scan'),
    path('result', leaderboard, name='leaderboard'),
    path('register/', register_for_hunt, name='register_for_hunt'),
    path('scan/<slug:code>', scan, name='scan'), 
    path('generate_qr', generate_qr, name='generate_qr'), 
    path('logout/', logout_view, name='logout'),
]