import requests
import json
from django.conf import settings
import PyPDF2
import docx
from io import BytesIO

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(file_content):
        """Extract text from PDF file"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_content):
        """Extract text from DOCX file"""
        try:
            docx_file = BytesIO(file_content)
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    @staticmethod
    def process_file(uploaded_file):
        """Process uploaded file and extract text"""
        file_content = uploaded_file.read()
        
        if uploaded_file.content_type == 'application/pdf':
            return FileProcessor.extract_text_from_pdf(file_content)
        elif uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return FileProcessor.extract_text_from_docx(file_content)
        else:
            raise Exception('Unsupported file type')

class AIAnalyzer:
    @staticmethod
    def analyze_resume(text):
        """Analyze resume text using OpenRouter API"""
        api_key = settings.OPENROUTER_API_KEY
        
        if not api_key:
            raise Exception('OpenRouter API key not configured')

        prompt = f"""Analyze the following resume text and provide a comprehensive evaluation. Return your response as a JSON object with the following structure:

{{
  "overallScore": number (0-100),
  "structureScore": number (0-100),
  "grammarScore": number (0-100), 
  "atsScore": number (0-100),
  "readabilityScore": number (0-100),
  "structureAnalysis": {{
    "score": number (0-100),
    "feedback": ["positive feedback item 1", "positive feedback item 2"],
    "suggestions": ["improvement suggestion 1", "improvement suggestion 2"]
  }},
  "grammarAnalysis": {{
    "score": number (0-100),
    "feedback": ["grammar feedback item 1", "grammar feedback item 2"],
    "suggestions": ["grammar improvement 1", "grammar improvement 2"]
  }},
  "atsAnalysis": {{
    "score": number (0-100),
    "feedback": ["ATS feedback item 1", "ATS feedback item 2"],
    "suggestions": ["ATS improvement 1", "ATS improvement 2"]
  }},
  "readabilityAnalysis": {{
    "score": number (0-100),
    "feedback": ["readability feedback item 1", "readability feedback item 2"],
    "suggestions": ["readability improvement 1", "readability improvement 2"]
  }}
}}

Please evaluate:
1. Structure: Layout, organization, formatting, section headers, consistency
2. Grammar: Spelling, grammar, punctuation, language usage
3. ATS Compatibility: Keyword optimization, standard section names, formatting compatibility
4. Readability: Clarity, conciseness, flow, bullet point usage

Resume text:
{text}"""

        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'localhost',
                    'X-Title': 'ResumeAI Analyzer'
                },
                json={
                    'model': 'openai/gpt-4o-mini',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are an expert resume analyzer. Provide detailed, actionable feedback in JSON format only.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.1,
                    'max_tokens': 2000
                }
            )

            if not response.ok:
                raise Exception(f'OpenRouter API error: {response.status_code} {response.text}')

            data = response.json()
            content = data['choices'][0]['message']['content']
            
            if not content:
                raise Exception('No response content from AI')

            # Clean JSON response if it contains markdown formatting
            if content.startswith('```json'):
                content = content.strip('```json').strip('```').strip()
            elif content.startswith('```'):
                content = content.strip('```').strip()

            # Parse JSON response
            analysis = json.loads(content)
            
            # Validate the response structure
            required_fields = ['overallScore', 'structureAnalysis', 'grammarAnalysis', 'atsAnalysis', 'readabilityAnalysis']
            for field in required_fields:
                if field not in analysis:
                    raise Exception(f'Missing required field: {field}')

            return analysis
        except json.JSONDecodeError as e:
            raise Exception(f'Invalid JSON response from AI: {str(e)}')
        except Exception as e:
            raise Exception(f'Failed to analyze resume with AI: {str(e)}')