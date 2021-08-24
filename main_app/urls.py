from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('about/', views.about, name="about"),
  path('cryptids/', views.cryptids_index, name='cryptids_index'),
  path('cryptids/<int:cryptid_id>/', views.cryptids_detail, name='cryptids_detail'),
  path('cryptids/create/', views.CryptidCreate.as_view(), name='cryptids_create'),
  path('cryptids/<int:pk>/update/', views.CryptidUpdate.as_view(), name='cryptids_update'),
  path('cryptids/<int:pk>/delete/', views.CryptidDelete.as_view(), name='cryptids_delete'),
  path('cryptids/<int:cryptid_id>/add_sighting/', views.add_sighting, name='add_sighting'),
  path('evidence/create/', views.EvidenceCreate.as_view(), name='evidence_create'),
  path('evidence/<int:pk>/', views.EvidenceDetail.as_view(), name='evidence_detail'),
  path('evidence/', views.EvidenceList.as_view(), name='evidence_index'),
  path('evidence/<int:pk>/update/', views.EvidenceUpdate.as_view(), name='evidence_update'),
  path('evidence/<int:pk>/delete/', views.EvidenceDelete.as_view(), name='evidence_delete'),
]
