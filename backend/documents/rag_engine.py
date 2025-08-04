import uuid
import openai
import chromadb
import re
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from django.conf import settings
from .models import Document, DocumentChunk


class RAGEngine:
    def __init__(self):
        # Initialize ChromaDB
        self.chroma_client = chromadb.HttpClient(host="chromadb.zeabur.internal", port=8000)
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
        """Split text into overlapping chunks with improved logic."""
        if not text or not text.strip():
            return []

        # Clean and normalize the text
        text = self._clean_text(text)

        # Try sentence-based chunking first
        chunks = self._chunk_by_sentences(text, chunk_size, overlap)

        # If sentence-based chunking fails or produces too few chunks, use paragraph-based
        if len(chunks) <= 1 and len(text) > chunk_size * 2:
            chunks = self._chunk_by_paragraphs(text, chunk_size, overlap)

        # If still not good, use word-based chunking as fallback
        if len(chunks) <= 1 and len(text) > chunk_size * 2:
            chunks = self._chunk_by_words(text, chunk_size, overlap)

        # Filter out very short chunks
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]

        # Return original text if all methods fail
        return chunks if chunks else [text]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Replace multiple whitespace characters with single space
        text = re.sub(r'\s+', ' ', text)

        # Remove excessive newlines but keep paragraph breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # Fix common PDF extraction issues
        text = text.replace('\n', ' ')  # Convert newlines to spaces
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space

        return text.strip()

    def _chunk_by_sentences(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Chunk text by sentences."""
        # More comprehensive sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)

        if len(sentences) <= 1:
            return []

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Add overlap from the end of current chunk
                if overlap > 0:
                    words = current_chunk.split()
                    overlap_words = words[-min(overlap, len(words)):]
                    current_chunk = ' '.join(overlap_words) + ' ' + sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk += (' ' if current_chunk else '') + sentence

        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _chunk_by_paragraphs(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Chunk text by paragraphs."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        if len(paragraphs) <= 1:
            return []

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Add overlap
                if overlap > 0:
                    words = current_chunk.split()
                    overlap_words = words[-min(overlap, len(words)):]
                    current_chunk = ' '.join(overlap_words) + ' ' + paragraph
                else:
                    current_chunk = paragraph
            else:
                current_chunk += ('\n\n' if current_chunk else '') + paragraph

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _chunk_by_words(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Chunk text by words (fallback method)."""
        words = text.split()

        if len(words) <= 10:  # Too few words to chunk meaningfully
            return []

        chunks = []
        # Convert character-based chunk_size to approximate word count
        # Rough estimate: 6 chars per word
        words_per_chunk = max(50, chunk_size // 6)
        overlap_words = max(5, overlap // 6)

        for i in range(0, len(words), words_per_chunk - overlap_words):
            chunk_words = words[i:i + words_per_chunk]
            if len(chunk_words) > 10:  # Only include chunks with sufficient content
                chunks.append(' '.join(chunk_words))

        return chunks

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text chunks."""
        if not texts:
            return []
        return self.embedding_model.encode(texts).tolist()

    def store_document_embeddings(self, document: Document, chunks: List[str]) -> None:
        """Store document chunks and their embeddings in ChromaDB."""
        if not chunks:
            print(f"No chunks to store for document {document.id}")
            return

        embeddings = self.generate_embeddings(chunks)

        if not embeddings:
            print(f"No embeddings generated for document {document.id}")
            return

        # Clear existing chunks for this document
        existing_chunks = DocumentChunk.objects.filter(document=document)
        embedding_ids = [chunk.embedding_id for chunk in existing_chunks]

        if embedding_ids:
            try:
                self.collection.delete(ids=embedding_ids)
            except Exception as e:
                print(f"Error deleting existing embeddings: {e}")

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
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(
                f"Successfully stored {len(chunks)} chunks for document {document.id}")
        except Exception as e:
            print(f"Error storing embeddings in ChromaDB: {e}")
            raise

    def similarity_search(self, query: str, document_id: int, num_results: int = 3) -> List[Dict[str, Any]]:
        """Perform similarity search for relevant chunks."""
        if not query or not document_id:
            return []

        try:
            query_embedding = self.generate_embeddings([query])
            if not query_embedding:
                return []

            # Get the first embedding (single query case)
            query_embedding = query_embedding[0] if query_embedding else None
            if query_embedding is None:
                return []

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=num_results,
                where={"document_id": document_id}
            )

            # Validate and process results
            if not results or not results.get('ids'):
                return []

            relevant_chunks = []
            for i in range(len(results['ids'][0])):
                try:
                    chunk_id = results['ids'][0][i]
                    if not chunk_id:
                        continue

                    chunk_data = {
                        'content': results['documents'][0][i],
                        'distance': results['distances'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {
                            'document_id': document_id,
                            'chunk_index': i
                        }
                    }
                    relevant_chunks.append(chunk_data)
                except (IndexError, KeyError):
                    continue

            return relevant_chunks

        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            return []

    def generate_answer(self, question: str, context_chunks: List[Dict[str, Any]], document_title: str) -> Dict[str, Any]:
        """Generate answer using the improved context processing."""
        # Validate input parameters
        if not question or not isinstance(question, str):
            return {
                'answer': "Invalid question provided.",
                'sources': [],
                'context_used': 0
            }

        if not context_chunks or not isinstance(context_chunks, list):
            return {
                'answer': "No relevant context was found to answer your question.",
                'sources': [],
                'context_used': 0
            }

        # Filter and validate chunks
        valid_chunks = []
        for chunk in context_chunks:
            try:
                if not chunk or not isinstance(chunk, dict):
                    continue

                content = chunk.get('content')
                metadata = chunk.get('metadata', {})

                if content and isinstance(content, str) and content.strip():
                    valid_chunks.append({
                        'content': content.strip(),
                        'metadata': metadata if isinstance(metadata, dict) else {}
                    })
            except Exception:
                continue

        if not valid_chunks:
            return {
                'answer': "The available context was not sufficient to answer your question.",
                'sources': [],
                'context_used': 0
            }

        # Prepare context for the prompt
        context_parts = []
        sources = []

        for i, chunk in enumerate(valid_chunks):
            try:
                chunk_content = chunk['content']
                chunk_index = chunk['metadata'].get('chunk_index', i)
                page_num = chunk['metadata'].get('page_number', 1)

                context_parts.append(
                    f"=== Excerpt from Document (Chunk {chunk_index + 1}, Page {page_num}) ===\n"
                    f"{chunk_content}\n"
                )

                sources.append({
                    'chunk_index': chunk_index,
                    'page_number': page_num,
                    'content_preview': chunk_content[:200] + '...' if len(chunk_content) > 200 else chunk_content,
                    'length': len(chunk_content)
                })
            except Exception:
                continue

        if not context_parts:
            return {
                'answer': "Could not extract valid context from the document.",
                'sources': [],
                'context_used': 0
            }

        context = "\n".join(context_parts)

        # Construct the prompt
        prompt = f"""You are an expert AI assistant analyzing the document titled "{document_title}".
Your task is to answer the user's question based ONLY on the provided context from the document.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
1. Answer concisely but thoroughly based ONLY on the provided context
2. If the question cannot be answered from the context, say so explicitly
3. If multiple chunks contain relevant information, synthesize them into a coherent answer
4. Maintain an academic tone and be precise with your information

ANSWER:"""

        try:
            # Call DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that provides accurate answers based on document content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1500,
                top_p=0.9
            )

            # Process the response
            if not response.choices:
                raise ValueError("No response generated from the model")

            answer = response.choices[0].message.content.strip()

            # Post-process the answer to ensure quality
            if not answer or answer.lower().startswith(("i don't know", "i couldn't find", "the context doesn't")):
                answer = "I couldn't find a definitive answer to your question in the document."

            return {
                'answer': answer,
                'sources': sources,
                'context_used': len(valid_chunks)
            }

        except Exception as e:
            error_msg = str(e)
            print(f"Error generating answer: {error_msg}")

            # Provide a helpful error message without exposing internal details
            return {
                'answer': "I encountered an issue generating the answer. Please try again with a different question or check the document content.",
                'sources': [],
                'context_used': 0
            }
