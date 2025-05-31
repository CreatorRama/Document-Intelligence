import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Document, DocumentChunk
from .serializers import (
    DocumentSerializer, 
    DocumentUploadSerializer, 
    QuestionSerializer
)
from .document_processor import DocumentProcessor
from .rag_engine import RAGEngine

# Initialize RAG engine
rag_engine = RAGEngine()

@api_view(['GET'])
def get_documents(request):
    """Retrieve all uploaded documents."""
    try:
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response({
            'success': True,
            'documents': serializer.data,
            'count': len(serializer.data)
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def upload_document(request):
    """Upload and process a document."""
    try:
        serializer = DocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        title = serializer.validated_data.get('title', os.path.splitext(file.name)[0])
        
        # Create document record
        document = Document.objects.create(
            title=title,
            file_type=os.path.splitext(file.name)[1].lower(),
            file_size=file.size,
            processing_status='processing'
        )
        
        # Save file
        document.file_path = file
        document.save()
        
        try:
            # Extract text from document
            text_content, page_count = DocumentProcessor.extract_text_from_file(file)
            document.pages = page_count
            
            # Chunk the text
            chunks = rag_engine.chunk_text(text_content)
            
            # Store embeddings
            rag_engine.store_document_embeddings(document, chunks)
            
            # Update status
            document.processing_status = 'completed'
            document.save()
            
            return Response({
                'success': True,
                'document': DocumentSerializer(document).data,
                'chunks_created': len(chunks)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as processing_error:
            document.processing_status = 'failed'
            document.save()
            return Response({
                'success': False,
                'error': f"Document processing failed: {str(processing_error)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ask_question(request):
    """Ask a question about a document using RAG."""
    try:
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        document_id = serializer.validated_data['document_id']
        question = serializer.validated_data['question']
        num_chunks = serializer.validated_data['num_chunks']
        
        # Get document
        document = get_object_or_404(Document, id=document_id)
        
        if document.processing_status != 'completed':
            return Response({
                'success': False,
                'error': 'Document is not ready for querying. Please wait for processing to complete.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform similarity search
        relevant_chunks = rag_engine.similarity_search(
            query=question,
            document_id=document_id,
            num_results=num_chunks
        )
        
        if not relevant_chunks:
            return Response({
                'success': False,
                'error': 'No relevant content found in the document for your question.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generate answer
        result = rag_engine.generate_answer(
            question=question,
            context_chunks=relevant_chunks,
            document_title=document.title
        )
        
        return Response({
            'success': True,
            'question': question,
            'answer': result['answer'],
            'sources': result['sources'],
            'document': {
                'id': document.id,
                'title': document.title
            },
            'context_chunks_used': result['context_used']
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def document_detail(request, document_id):
    """Get detailed information about a specific document."""
    try:
        document = get_object_or_404(Document, id=document_id)
        chunks = DocumentChunk.objects.filter(document=document)
        
        return Response({
            'success': True,
            'document': DocumentSerializer(document).data,
            'total_chunks': chunks.count(),
            'chunks_sample': [
                {
                    'index': chunk.chunk_index,
                    'content_preview': chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                    'page_number': chunk.page_number
                }
                for chunk in chunks[:3]  # Show first 3 chunks as sample
            ]
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)