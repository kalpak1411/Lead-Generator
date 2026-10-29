from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('leads/', views.lead_list_view, name='lead_list'),
    path('leads/add/', views.lead_create_view, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail_view, name='lead_detail'),
    path('leads/<int:pk>/research/', views.lead_research_view, name='lead_research'),
    path('icps/', views.icp_list_view, name='icp_list'),
    path('export/csv/', views.export_leads_csv, name='export_csv'),
]

