from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('cryptids/', views.cryptids_index, name='cryptids_index'),
  path('cryptids/<int:cryptid_id>/', views.cryptids_detail, name='cryptids_detail'),
]
