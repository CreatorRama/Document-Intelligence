'use client'
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Document Upload - POST to /api/documents/upload/
export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post('/documents/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Get All Documents - GET /api/documents/
export const fetchDocuments = async () => {
  const response = await apiClient.get('/documents/');
  return response.data;
};

// Ask Question - POST /api/ask/
export const askQuestion = async (documentId: string, question: string, numChunks = 3) => {
  const response = await apiClient.post('/ask/', {
    document_id: documentId,
    question: question,
    num_chunks: numChunks,
  });
  return response.data;
};

// Get Document details - GET /api/documents/{id}/
export const getDocumentDetails = async (documentId: string) => {
  const response = await apiClient.get(`/documents/${documentId}/`);
  return response.data;
};

export default apiClient;