from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.get_documents, name='get_documents'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
    path('ask/', views.ask_question, name='ask_question'),
]