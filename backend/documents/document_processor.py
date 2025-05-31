import os
import PyPDF2
import docx
from typing import Tuple, List
from django.core.files.uploadedfile import UploadedFile

class DocumentProcessor:
    @staticmethod
    def extract_text_from_file(file: UploadedFile) -> Tuple[str, int]:
        """Extract text from uploaded file and return text and page count."""
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension == '.txt':
            return DocumentProcessor._extract_from_txt(file), 1
        elif file_extension == '.pdf':
            return DocumentProcessor._extract_from_pdf(file)
        elif file_extension in ['.docx', '.doc']:
            return DocumentProcessor._extract_from_docx(file), 1
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def _extract_from_txt(file: UploadedFile) -> str:
        """Extract text from TXT file."""
        return file.read().decode('utf-8')
    
    @staticmethod
    def _extract_from_pdf(file: UploadedFile) -> Tuple[str, int]:
        """Extract text from PDF file."""
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        page_count = len(pdf_reader.pages)
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text, page_count
    
    @staticmethod
    def _extract_from_docx(file: UploadedFile) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text