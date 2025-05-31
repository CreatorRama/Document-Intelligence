// app/dashboard/page.tsx
import DocumentList from './components/DocumentList'
import { fetchDocumentsServer } from '../lib/server-api'
import { Suspense } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'

export default async function DashboardPage() {
  try {
    const data = await fetchDocumentsServer()
    
    return (
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
          <a
            href="/upload"
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
          >
            Upload Document
          </a>
        </div>

        <Suspense fallback={<LoadingSpinner />}>
          <DocumentList documents={data} />
        </Suspense>
      </div>
    )
  } catch (error) {
    return (
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
          <a
            href="/upload"
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
          >
            Upload Document
          </a>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800">Failed to load documents. Please try refreshing the page.</p>
        </div>
      </div>
    )
  }
}