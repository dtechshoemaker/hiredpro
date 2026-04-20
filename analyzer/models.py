from django.db import models
from django.contrib.auth.models import User
import json

class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_analyses')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    extracted_text = models.TextField()
    
    # Scores
    overall_score = models.IntegerField()
    structure_score = models.IntegerField()
    grammar_score = models.IntegerField()
    ats_score = models.IntegerField()
    readability_score = models.IntegerField()
    
    # Analysis results (stored as JSON)
    structure_analysis = models.JSONField()
    grammar_analysis = models.JSONField()
    ats_analysis = models.JSONField()
    readability_analysis = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.file_name} - {self.overall_score}/100"