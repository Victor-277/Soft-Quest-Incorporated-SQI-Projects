from django.contrib import admin
from django.urls import path, include, re_path
from investmentApp.userapp import views as vw

urlpatterns = [
    re_path(r'^my_profile/(?P<u_id>\d+)/',  vw.myProfile, name='my_profile'),
    re_path(r'^edit_profile/(?P<u_id>\d+)/',  vw.myProfile, name='edit_profile'),
    re_path(r'^deactivate_profile/(?P<u_id>\d+)/',  vw.myProfile, name='deactivate_profile'),
]