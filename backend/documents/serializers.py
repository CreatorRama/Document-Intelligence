from rest_framework import serializers
from .models import Document, DocumentChunk

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_type', 'file_size', 'pages', 'processing_status', 'created_at']

class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['id', 'chunk_index', 'content', 'page_number']

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(max_length=255, required=False)

class QuestionSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    question = serializers.CharField()
    num_chunks = serializers.IntegerField(default=3, min_value=1, max_value=10)