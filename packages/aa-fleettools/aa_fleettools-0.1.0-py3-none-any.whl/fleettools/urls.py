from django.urls import path

from . import views

app_name = 'fleettools'

urlpatterns = [
    path('', views.index, name='index'),
    path('fleetmover/', views.fleetmoverlogin, name='fleetmoverlogin'),
    path('fleetmover/<int:token_pk>/', views.fleetmover, name='fleetmover'),
    path('fleetmover/button/<int:token_pk>/<int:fleet_id>/<int:wing_id>/<int:squad_destination_id>/<int:wing_destination_id>/', views.buttonmover, name='buttonmover'),
]
