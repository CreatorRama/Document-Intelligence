import os
import PyPDF2
import docx
from typing import Tuple, List
from django.core.files.uploadedfile import UploadedFile
import re

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
        """Extract text from PDF file with improved processing."""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    # Extract text from page
                    page_text = page.extract_text()
                    
                    if page_text:
                        # Clean the extracted text
                        cleaned_text = DocumentProcessor._clean_pdf_text(page_text)
                        
                        # Add page marker for better organization
                        text += f"\n=== Page {page_num + 1} ===\n{cleaned_text}\n"
                    
                except Exception as e:
                    print(f"Error extracting text from page {page_num + 1}: {e}")
                    continue
            
            # Final text processing
            final_text = DocumentProcessor._post_process_extracted_text(text)
            
            return final_text, page_count
            
        except Exception as e:
            print(f"PDF extraction error: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    @staticmethod  
    def _clean_pdf_text(text: str) -> str:
        """Clean PDF extracted text to make it more readable."""
        if not text:
            return ""
        
        # Step 1: Handle common PDF extraction issues
        # Fix words that got concatenated (no space between words)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Fix number-letter combinations
        text = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', text)
        
        # Step 2: Clean up whitespace
        # Replace multiple spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Clean up newlines - preserve paragraph breaks but remove excessive newlines
        text = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', text)  # Multiple newlines -> double newline
        text = re.sub(r'\n[ \t]+', '\n', text)  # Remove spaces after newlines
        
        # Step 3: Fix common formatting issues
        # Add space after periods if missing (for sentences)
        text = re.sub(r'\.([A-Z])', r'. \1', text)
        
        # Fix bullet points and list items
        text = re.sub(r'•\s*', '• ', text)
        text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]\s*', '• ', text)  # Various bullet Unicode
        
        # Step 4: Handle email and URL formatting
        text = re.sub(r'([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})', r'\1@\2.\3', text)
        
        return text.strip()
    
    @staticmethod
    def _post_process_extracted_text(text: str) -> str:
        """Final processing to improve text structure."""
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip very short lines that are likely formatting artifacts
            if len(line) < 2:
                continue
                
            # Skip lines with only special characters or numbers
            if re.match(r'^[^a-zA-Z]*$', line):
                continue
            
            # Add the line
            processed_lines.append(line)
        
        # Join lines back together
        result = '\n'.join(processed_lines)
        
        # Final cleanup
        result = re.sub(r'\n{3,}', '\n\n', result)  # Max 2 consecutive newlines
        
        # Ensure sections are properly separated
        result = re.sub(r'(===.*?===)', r'\n\1\n', result)
        
        return result.strip()
    
    @staticmethod
    def _extract_from_docx(file: UploadedFile) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file)
        text = ""
        
        for paragraph in doc.paragraphs:
            para_text = paragraph.text.strip()
            if para_text:  # Only add non-empty paragraphs
                text += para_text + "\n"
        
        return DocumentProcessor._post_process_extracted_text(text)