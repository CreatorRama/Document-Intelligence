from django.contrib import admin
from .models import Document, DocumentChunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type', 'pages', 'processing_status', 'created_at']
    list_filter = ['file_type', 'processing_status', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['document', 'chunk_index', 'page_number', 'created_at']
    list_filter = ['document', 'page_number']
    search_fields = ['document__title', 'content']
