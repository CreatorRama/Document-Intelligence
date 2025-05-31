import os
import uuid
import openai
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from django.conf import settings
from .models import Document, DocumentChunk

class RAGEngine:
    def __init__(self):
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name="document_embeddings",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Configure DeepSeek API
        self.client = openai.OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks."""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Add overlap
                words = current_chunk.split()
                overlap_words = words[-overlap:] if len(words) > overlap else words
                current_chunk = ' '.join(overlap_words) + '. ' + sentence
            else:
                current_chunk += sentence + '. '
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text chunks."""
        return self.embedding_model.encode(texts).tolist()
    
    def store_document_embeddings(self, document: Document, chunks: List[str]) -> None:
        """Store document chunks and their embeddings in ChromaDB."""
        embeddings = self.generate_embeddings(chunks)
        
        # Clear existing chunks for this document
        existing_chunks = DocumentChunk.objects.filter(document=document)
        embedding_ids = [chunk.embedding_id for chunk in existing_chunks]
        
        if embedding_ids:
            try:
                self.collection.delete(ids=embedding_ids)
            except:
                pass  # Continue if deletion fails
        
        existing_chunks.delete()
        
        # Store new chunks
        ids = []
        metadatas = []
        documents = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            embedding_id = str(uuid.uuid4())
            
            # Store in ChromaDB
            ids.append(embedding_id)
            metadatas.append({
                'document_id': document.id,
                'chunk_index': i,
                'document_title': document.title
            })
            documents.append(chunk)
            
            # Store in MySQL
            DocumentChunk.objects.create(
                document=document,
                chunk_index=i,
                content=chunk,
                embedding_id=embedding_id
            )
        
        # Add to ChromaDB collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def similarity_search(self, query: str, document_id: int, num_results: int = 3) -> List[Dict[str, Any]]:
            """Perform similarity search for relevant chunks."""
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Check if collection has documents for this document_id
            try:
                count_result = self.collection.count()
                if count_result == 0:
                    return []
                
                # Search in ChromaDB with document filter
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=min(num_results, count_result),  # Don't request more than available
                    where={"document_id": document_id}
                )
                
                if not results['ids'][0]:  # No results found
                    return []
                    
                relevant_chunks = []
                for i in range(len(results['ids'][0])):
                    chunk_data = {
                        'content': results['documents'][0][i],
                        'distance': results['distances'][0][i],
                        'metadata': results['metadatas'][0][i]
                    }
                    relevant_chunks.append(chunk_data)
                
                return relevant_chunks
                
            except Exception as e:
                print(f"Error in similarity search: {e}")
                return []
    def generate_answer(self, question: str, context_chunks: List[Dict[str, Any]], document_title: str) -> Dict[str, Any]:
            """Generate answer using DeepSeek API with context."""
            
            if not context_chunks:
                return {
                    'answer': "I couldn't find relevant information in the document to answer your question.",
                    'sources': [],
                    'context_used': 0
                }
            
            # Prepare context from chunks
            context = "\n\n".join([
                f"[Chunk {chunk['metadata']['chunk_index'] + 1}]: {chunk['content']}"
                for chunk in context_chunks
            ])
                
            prompt = f"""You are an AI assistant helping users understand documents. Based on the provided context from the document "{document_title}", answer the user's question accurately and comprehensively.

        Context from document:
        {context}

        Question: {question}

        Instructions:
        1. Answer the question based solely on the provided context
        2. If the context doesn't contain enough information to answer the question, say so clearly
        3. Cite relevant chunks when making specific claims (e.g., "According to Chunk 2...")
        4. Be concise but thorough
        5. If multiple chunks contain relevant information, synthesize them coherently

        Answer:"""

            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that answers questions based on document content."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                
                answer = response.choices[0].message.content
                
                return {
                    'answer': answer,
                    'sources': [
                        {
                            'chunk_index': chunk['metadata']['chunk_index'],
                            'content_preview': chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'],
                            'similarity_score': 1 - chunk['distance']
                        }
                        for chunk in context_chunks
                    ],
                    'context_used': len(context_chunks)
                }
                
            except Exception as e:
                return {
                    'answer': f"I apologize, but I encountered an error while generating the answer: {str(e)}",
                    'sources': [],
                    'context_used': 0
                }