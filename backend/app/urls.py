from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout_view, name='logout'),
    path('main/', main_view, name='main'),
    path('about-machine/<int:machine_id>/', about_machine, name='about_machine'),
    path('get_description/', get_description, name='get_description'),
]