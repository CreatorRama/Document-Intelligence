# Document Intelligence Backend

A Django-based REST API system that enables intelligent document processing and question-answering using RAG (Retrieval-Augmented Generation) technology. Upload documents and ask questions to get contextual answers based on document content.

## 🚀 Features

- **Document Upload & Processing**: Support for PDF, DOCX, and TXT files
- **Intelligent Q&A**: Ask questions about your documents using natural language
- **RAG Implementation**: Advanced retrieval-augmented generation for accurate answers
- **Vector Search**: ChromaDB integration for semantic similarity search
- **REST API**: Full REST API with Django REST Framework
- **Document Management**: Track processing status and document metadata

## 📁 Project Structure

```
backend/
│
├── 📁 document_intelligence/          # Main Django project directory
│   ├── settings.py                    # Django settings & configuration
│   ├── urls.py                        # Main URL routing
│   └── wsgi.py                        # WSGI configuration
│
├── 📁 documents/                      # Django app for document handling
│   ├── models.py                      # Database models (Document, DocumentChunk)
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # API view functions
│   ├── urls.py                        # App URL routing
│   ├── document_processor.py          # Document text extraction
│   └── rag_engine.py                  # RAG pipeline implementation
│
├── 📁 media/documents/                # Uploaded documents storage
├── 📁 chroma_db/                      # ChromaDB vector database(automatically created)
├── 📁 staticfiles/                    # Django static files
├── .env                               # Environment variables
├── requirements.txt                   # Python dependencies
└── manage.py                          # Django management script
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE document_intelligence;
CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON document_intelligence.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
MYSQL_PASSWORD=your_mysql_password
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 6. Update Database Configuration

Update `settings.py` with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'document_intelligence',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 7. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📋 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. Get All Documents
```http
GET /documents/
```

**Response:**
```json
{
  "success": true,
  "documents": [
    {
      "id": 1,
      "title": "Sample Document",
      "file_type": ".pdf",
      "file_size": 1024000,
      "pages": 5,
      "processing_status": "completed",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

#### 2. Upload Document
```http
POST /documents/upload/
Content-Type: multipart/form-data
```

**Request:**
```
file: [document file]
title: "Optional Document Title"
```

**Response:**
```json
{
  "success": true,
  "document": {
    "id": 1,
    "title": "Document Title",
    "processing_status": "completed"
  },
  "chunks_created": 25
}
```

#### 3. Ask Question
```http
POST /ask/
Content-Type: application/json
```

**Request:**
```json
{
  "document_id": 1,
  "question": "What are the main topics discussed?",
  "num_chunks": 3
}
```

**Response:**
```json
{
  "success": true,
  "question": "What are the main topics discussed?",
  "answer": "Based on the document content, the main topics include...",
  "sources": [
    {
      "chunk_index": 0,
      "content_preview": "Content preview...",
      "similarity_score": 0.85
    }
  ],
  "document": {
    "id": 1,
    "title": "Document Title"
  },
  "context_chunks_used": 3
}
```

#### 4. Get Document Details
```http
GET /documents/{document_id}/
```

**Response:**
```json
{
  "success": true,
  "document": {
    "id": 1,
    "title": "Document Title",
    "processing_status": "completed"
  },
  "total_chunks": 25,
  "chunks_sample": [
    {
      "index": 0,
      "content_preview": "First chunk content...",
      "page_number": 1
    }
  ]
}
```

## 🤖 Sample Questions and Answers

Based on a resume document, here are example interactions:

### Question 1: Frontend Skills
**Q:** "What are my frontend skills?"

**A:** Based on the provided context, your frontend skills include:
- **React.js**
- **Next.js** 
- **Redux**
- **Tailwind CSS**
- **Canvas API**
- **SVG Animations**

These skills are listed under the "Frontend Development" section in the document.

### Question 2: Backend Skills
**Q:** "What are my backend skills?"

**A:** Based on the provided context, your backend skills include:

1. **Backend Development**:
   - Flask
   - Node.js
   - Express.js
   - Django

2. **Databases**:
   - MongoDB
   - SQL
   - Sequelize ORM
   - Mongoose ODM

3. **APIs**:
   - REST APIs

These skills are listed under the "Skills" section in the document.

### Question 3: Personal Information
**Q:** "What is my address?"

**A:** Based on the provided context from the document, your address is:
**Dasna, Ghaziabad, 201015, U.P.**

### Question 4: Programming Languages
**Q:** "What programming languages do I know?"

**A:** Based on the provided context, you know the following programming languages:

1. **C++**
2. **Python**
3. **Java**
4. **TypeScript**

These are listed under the "Skills" section in the "Other Languages" category.

### Question 5: Education Background
**Q:** "What is my education?"

**A:** Based on the provided context, your education includes:

1. **B.C.A in Computer Science** at JMS Group of Institution (August 2022 - Present) with a CGPA of 7.5.

2. **Additional Learning** in:
   - **DSA (Data Structures and Algorithms)**: Through LeetCode and PwSkills
   - **Full-Stack Development**: Self-taught via YouTube, documentation, ChatGPT, and self-study

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API key for AI responses | Yes |
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No |
| `MYSQL_PASSWORD` | MySQL database password | Yes |

### Supported File Types

- **PDF** (.pdf) - Extracted using PyPDF2
- **Word Documents** (.docx, .doc) - Extracted using python-docx
- **Text Files** (.txt) - Direct text reading

## 🚀 Technology Stack

- **Backend Framework**: Django 4.x + Django REST Framework
- **Database**: MySQL (metadata) + ChromaDB (vector storage)
- **AI/ML**: 
  - DeepSeek API for text generation
  - SentenceTransformers for embeddings
  - ChromaDB for vector similarity search
- **Document Processing**: PyPDF2, python-docx
- **Authentication**: Django built-in auth system

## 📊 Performance Considerations

- **Chunking Strategy**: 500 characters per chunk with 50-character overlap
- **Embedding Model**: all-MiniLM-L6-v2 (efficient and accurate)
- **Vector Database**: ChromaDB with cosine similarity
- **API Rate Limiting**: Consider implementing for production use

## 🛡️ Security Notes

- Store API keys in environment variables
- Use HTTPS in production
- Implement proper authentication/authorization
- Validate file uploads (size, type, content)
- Sanitize user inputs

## 🔄 Development Workflow

1. **Upload Document**: POST to `/documents/upload/`
2. **Check Processing**: GET `/documents/` to verify status
3. **Ask Questions**: POST to `/ask/` with document_id and question
4. **Review Sources**: Check returned sources for transparency

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **MySQL Connection Error**: Verify database credentials and server status
2. **File Upload Fails**: Check file size limits and supported formats
3. **ChromaDB Issues**: Ensure write permissions for `chroma_db/` directory
4. **API Key Errors**: Verify DeepSeek API key is valid and has sufficient credits

### Support

For technical support or questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ using Django, ChromaDB, and DeepSeek AI**