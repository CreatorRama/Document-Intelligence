import Link from 'next/link'
import { Document } from '../../lib/types'
import { formatBytes } from '../../lib/utils/index'
import { format } from 'date-fns'
import StatusBadge from '../../components/StatusBadge'

interface DocumentCardProps {
  document: Document
}

export default function DocumentCard({ document }: DocumentCardProps) {
  return (
    <Link
      href={`/qa?documentId=${document.id}`}
      className="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden"
    >
      <div className="p-6 space-y-4">
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-medium text-gray-900 truncate">
            {document.title}
          </h3>
          <StatusBadge status={document.processing_status} />
        </div>

        <div className="flex items-center text-sm text-gray-500">
          <span className="capitalize">{document.file_type}</span>
          <span className="mx-2">•</span>
          <span>{formatBytes(document.file_size)}</span>
          {document.pages_count > 0 && (
            <>
              <span className="mx-2">•</span>
              <span>{document.pages_count} pages</span>
            </>
          )}
        </div>

        <div className="flex justify-between items-center text-sm text-gray-500">
          <span>{format(new Date(document.created_at), 'MMM d, yyyy')}</span>
          <span>{document.chunks_count || 0} chunks</span>
        </div>
      </div>
    </Link>
  )
}