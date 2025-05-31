'use client'

import { useSearchParams } from 'next/navigation'
import QASection from './components/QASection'
import { Suspense } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'

export default function QAPage() {
  const searchParams = useSearchParams()
  const documentId = searchParams.get('documentId')

  if (!documentId) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No document selected.</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <Suspense fallback={<LoadingSpinner />}>
        <QASection documentId={documentId} />
      </Suspense>
    </div>
  )
}