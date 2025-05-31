export interface Document {
  id: string
  title: string
  file_type: string
  file_size: number
  pages_count: number
  processing_status: 'processing' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  chunks_count?: number
}

export interface DocumentChunk {
  id: string
  chunk_index: number
  content: string
  page_number?: number
}

// In your types file
export interface QuestionResponse {
  answer: string;
  confidence: number;
  sources: Array<{
    chunk_index: number       
    content_preview: string           
    similarity_score: number 
  }>;
  relevant_chunks?: string[];
}

export interface UploadResponse {
  id: string
  title: string
  file_type: string
  file_size: number
  pages_count: number
  processing_status: string
  created_at: string
  updated_at: string
}