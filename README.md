# ResumeAI - AI-Powered Resume Analysis Platform

This repository contains **two complete implementations** of an AI-powered resume analyzer:

1. **React + Express.js version** (Primary) - Located in `client/`, `server/`, and `shared/`
2. **Django version** (Alternative) - Located in `resumeai_django/`, `analyzer/`, `authentication/`, and `templates/`

Both versions provide identical functionality with the same modern design and comprehensive features.

## 🚀 Features

- **User Authentication** - Secure login/signup system
- **File Upload** - Support for PDF and DOCX resume files (up to 10MB)
- **AI Analysis** - Comprehensive evaluation using OpenRouter's GPT-4o-mini model
- **Score Breakdown** - Detailed scoring across 4 dimensions:
  - Structure Analysis (layout, organization, formatting)
  - Grammar Check (spelling, grammar, language usage)
  - ATS Optimization (keyword optimization, compatibility)
  - Readability Score (clarity, conciseness, flow)
- **Detailed Feedback** - Specific suggestions for improvement
- **Analysis History** - View past analyses and track progress
- **Responsive Design** - Beautiful UI with responsive CSS
- **Real-time Processing** - Instant analysis results

## 🏗️ Technology Stack

### React + Express.js Version
- **Frontend**: React 18, TypeScript, Vite, Shadcn/ui
- **Backend**: Node.js, Express.js, TypeScript
- **Database**: PostgreSQL with Drizzle ORM
- **Authentication**: Replit Auth (OpenID Connect)
- **File Processing**: pdf-parse, mammoth
- **AI**: OpenRouter API integration

### Django Version
- **Frontend**: Django Templates, pure CSS
- **Backend**: Django 5.2, Django REST Framework
- **Database**: PostgreSQL with Django ORM
- **Authentication**: Django's built-in User system
- **File Processing**: PyPDF2, python-docx
- **AI**: OpenRouter API integration

## 🔧 Environment Variables Required

Create a local `.env` file for secrets and machine-specific settings. Do not commit `.env`; use `.env.example` as the safe template for other developers.

```env
SECRET_KEY=your_django_secret_key
DEBUG=true
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional PostgreSQL settings. If these are blank, Django uses local SQLite.
PGDATABASE=
PGUSER=
PGPASSWORD=
PGHOST=localhost
PGPORT=5432
```

**React version additionally needs:**
```env
SESSION_SECRET=your_session_secret
REPL_ID=your_repl_id
```

## 🚀 Quick Start

### React + Express.js Version (Recommended)

1. **Install dependencies:**
```bash
npm install
```

2. **Run database migrations:**
```bash
npm run db:push
```

3. **Start the application:**
```bash
npm run dev
```

The application will be available at `http://localhost:5000`

### Django Version

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

4. **Create a superuser (optional):**
```bash
python manage.py createsuperuser
```

5. **Start the Django server:**
```bash
python manage.py runserver 0.0.0.0:8000
```

The Django application will be available at `http://localhost:8000`

## Render Deployment

This project includes Render config files:

- `render.yaml` creates a web service and a PostgreSQL database.
- `build.sh` installs dependencies, collects static files, and runs migrations.
- `Procfile` starts Django with Gunicorn.
- `runtime.txt` pins the Python version.

In Render, set these environment variables as secrets:

```env
SECRET_KEY=your_django_secret_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Render will provide `DATABASE_URL` automatically when you deploy from `render.yaml`. Keep `.env` local only; do not push it to GitHub.

## 📱 Usage

1. **Sign up** for a new account or **log in** to existing account
2. **Upload your resume** in PDF or DOCX format
3. **Wait for AI analysis** (typically takes 10-30 seconds)
4. **Review detailed results** with scores and suggestions
5. **View analysis history** and track improvements over time

## 🎯 Analysis Dimensions

### Structure Analysis (0-100)
- Layout and visual organization
- Section headers and consistency
- Professional formatting
- Information hierarchy

### Grammar Analysis (0-100)
- Spelling and grammar errors
- Punctuation and syntax
- Language usage and clarity
- Professional tone

### ATS Analysis (0-100)
- Keyword optimization
- Standard section names
- Formatting compatibility
- Applicant Tracking System readiness

### Readability Analysis (0-100)
- Content clarity and conciseness
- Bullet point usage
- Flow and structure
- Overall readability score

## 🔒 Security Features

- **Secure Authentication** - Session-based auth with CSRF protection
- **File Validation** - Type and size restrictions
- **API Rate Limiting** - Prevents abuse
- **Data Privacy** - User data is isolated and secure

## 🎨 Design Features

- **Modern UI** - Clean, professional interface
- **Responsive Design** - Works on all device sizes
- **Dark/Light Mode** - Automatic theme detection
- **Interactive Elements** - Drag & drop file upload
- **Loading States** - Clear feedback during processing
- **Error Handling** - User-friendly error messages

## 📊 File Support

- **PDF Files** - Full text extraction support
- **DOCX Files** - Microsoft Word document support
- **File Size Limit** - Maximum 10MB per file
- **Batch Processing** - Multiple analyses per user

## 🚀 Deployment

Both versions are configured for easy deployment:

### React + Express.js
- **Vite Build** - Optimized production assets
- **Express Server** - Production-ready backend
- **Database Migrations** - Automatic schema management

### Django
- **Static Files** - WhiteNoise for static file serving
- **Database** - PostgreSQL production configuration
- **WSGI** - Ready for production deployment

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
- Check the documentation in `replit.md`
- Review the code comments for implementation details
- Ensure all environment variables are properly configured

---

**Note**: Both implementations provide identical functionality. Choose the React + Express.js version for modern full-stack development or the Django version for Python-based workflows.# hiredpro
