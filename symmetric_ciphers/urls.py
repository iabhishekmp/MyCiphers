from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/stream_cipher', views.stream, name='stream'),
    path('/stream_cipher/ceaser', views.ceaser, name='ceaser'),
    path('/stream_cipher/ceaser/ceaser_exi', views.ceaser_exicute, name='ceaser_exicute'),
    path('/stream_cipher/monoalphabetic', views.monoalphabetic, name='monoalphabetic'),
    path('/stream_cipher/monoalphabetic/monoalphabetic_exi', views.monoalphabetic_exicute, name='monoalphabetic_exicute'),
    path('/stream_cipher/polyalphabetic', views.polyalphabetic, name='polyalphabetic'),
    path('/stream_cipher/polyalphabetic/polyalphabetic_exi', views.polyalphabetic_exicute, name='polyalphabetic_exicute'),
    path('/stream_cipher/hill', views.hill, name='hill'),
    path('/stream_cipher/hill/hill_exi', views.hill_exicute, name='hill_exicute'),
    path('/stream_cipher/playfair', views.playfair, name='playfair'),
    path('/stream_cipher/playfair/playfair_exi', views.playfair_exicute, name='playfair_exicute'),


]