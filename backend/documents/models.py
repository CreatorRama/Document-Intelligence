from django.db import models
from django.utils import timezone

class Document(models.Model):
    PROCESSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=10)
    file_size = models.BigIntegerField()
    pages = models.IntegerField(default=0)
    processing_status = models.CharField(
        max_length=20, 
        choices=PROCESSING_STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['-created_at']

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    content = models.TextField()
    page_number = models.IntegerField(default=1)
    embedding_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"
    
    class Meta:
        ordering = ['chunk_index']
        unique_together = ['document', 'chunk_index']