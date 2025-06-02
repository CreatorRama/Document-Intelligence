'use client'
import axios from 'axios';

const API_BASE_URL = ' https://weed-divorce-sd-sega.trycloudflare.com/api';
if (!API_BASE_URL) {
  throw new Error('NEXT_PUBLIC_API_BASE_URL environment variable is not set');
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Helper function for error handling
const handleApiError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    throw new Error(
      error.response?.data?.message || 
      error.message || 
      'API request failed'
    );
  }
  throw new Error('An unexpected error occurred');
};

// Document Upload
export const uploadDocument = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/documents/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

// Get All Documents
export const fetchDocuments = async () => {
  try {
    const response = await apiClient.get('/documents/');
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

// Ask Question
export const askQuestion = async (documentId: string, question: string, numChunks = 3) => {
  try {
    const response = await apiClient.post('/ask/', {
      document_id: documentId,
      question,
      num_chunks: numChunks,
    });
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

// Get Document details
export const getDocumentDetails = async (documentId: string) => {
  try {
    const response = await apiClient.get(`/documents/${documentId}/`);
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

export default apiClient;