from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

from .models import ResumeAnalysis
from .services import FileProcessor, AIAnalyzer

def landing(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'analyzer/landing.html')

@login_required
def dashboard(request):
    """Dashboard page for authenticated users"""
    analyses = ResumeAnalysis.objects.filter(user=request.user)[:5]  # Last 5 analyses
    return render(request, 'analyzer/dashboard.html', {'analyses': analyses})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_resume(request):
    """API endpoint to analyze uploaded resume"""
    try:
        if 'resume' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['resume']
        
        # Validate file type
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if uploaded_file.content_type not in allowed_types:
            return Response({'error': 'Only PDF and DOCX files are allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return Response({'error': 'File size must be less than 10MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract text from file
        extracted_text = FileProcessor.process_file(uploaded_file)
        
        # Analyze with AI
        analysis_result = AIAnalyzer.analyze_resume(extracted_text)
        
        # Save to database
        resume_analysis = ResumeAnalysis.objects.create(
            user=request.user,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            extracted_text=extracted_text,
            overall_score=analysis_result['overallScore'],
            structure_score=analysis_result['structureScore'],
            grammar_score=analysis_result['grammarScore'],
            ats_score=analysis_result['atsScore'],
            readability_score=analysis_result['readabilityScore'],
            structure_analysis=analysis_result['structureAnalysis'],
            grammar_analysis=analysis_result['grammarAnalysis'],
            ats_analysis=analysis_result['atsAnalysis'],
            readability_analysis=analysis_result['readabilityAnalysis'],
        )
        
        # Return analysis data
        return Response({
            'id': resume_analysis.id,
            'fileName': resume_analysis.file_name,
            'fileSize': resume_analysis.file_size,
            'overallScore': resume_analysis.overall_score,
            'structureScore': resume_analysis.structure_score,
            'grammarScore': resume_analysis.grammar_score,
            'atsScore': resume_analysis.ats_score,
            'readabilityScore': resume_analysis.readability_score,
            'structureAnalysis': resume_analysis.structure_analysis,
            'grammarAnalysis': resume_analysis.grammar_analysis,
            'atsAnalysis': resume_analysis.ats_analysis,
            'readabilityAnalysis': resume_analysis.readability_analysis,
            'createdAt': resume_analysis.created_at.isoformat(),
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analyses(request):
    """API endpoint to get user's resume analyses"""
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    data = []
    
    for analysis in analyses:
        data.append({
            'id': analysis.id,
            'fileName': analysis.file_name,
            'fileSize': analysis.file_size,
            'overallScore': analysis.overall_score,
            'structureScore': analysis.structure_score,
            'grammarScore': analysis.grammar_score,
            'atsScore': analysis.ats_score,
            'readabilityScore': analysis.readability_score,
            'structureAnalysis': analysis.structure_analysis,
            'grammarAnalysis': analysis.grammar_analysis,
            'atsAnalysis': analysis.ats_analysis,
            'readabilityAnalysis': analysis.readability_analysis,
            'createdAt': analysis.created_at.isoformat(),
        })
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analysis(request, analysis_id):
    """API endpoint to get specific analysis"""
    try:
        analysis = ResumeAnalysis.objects.get(id=analysis_id, user=request.user)
        return Response({
            'id': analysis.id,
            'fileName': analysis.file_name,
            'fileSize': analysis.file_size,
            'overallScore': analysis.overall_score,
            'structureScore': analysis.structure_score,
            'grammarScore': analysis.grammar_score,
            'atsScore': analysis.ats_score,
            'readabilityScore': analysis.readability_score,
            'structureAnalysis': analysis.structure_analysis,
            'grammarAnalysis': analysis.grammar_analysis,
            'atsAnalysis': analysis.ats_analysis,
            'readabilityAnalysis': analysis.readability_analysis,
            'createdAt': analysis.created_at.isoformat(),
        })
    except ResumeAnalysis.DoesNotExist:
        return Response({'error': 'Analysis not found'}, status=status.HTTP_404_NOT_FOUND)