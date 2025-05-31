// components/DocumentList.tsx
import DocumentCard from './DocumentCard'
import { Document } from '../../lib/types'

interface DocumentListProps {
  documents: {
    success: boolean;
    documents: Document[];
    count: number;
  }
}

export default function DocumentList({ documents }: DocumentListProps) {
  console.log(documents)
  
  if (!documents.success || documents.count === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No documents uploaded yet.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {documents.documents.map((document) => (
        <DocumentCard key={document.id} document={document} />
      ))}
    </div>
  )
}