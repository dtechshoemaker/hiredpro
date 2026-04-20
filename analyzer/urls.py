from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/analyze-resume/', views.analyze_resume, name='analyze_resume'),
    path('api/analyses/', views.get_analyses, name='get_analyses'),
    path('api/analyses/<int:analysis_id>/', views.get_analysis, name='get_analysis'),
]