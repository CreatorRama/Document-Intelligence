'use client' 

import { Suspense } from 'react'
import QASection from './components/QASection'
import LoadingSpinner from '../components/LoadingSpinner'

export default function QAPage() {
  return (
    <div className="space-y-8">
      <Suspense fallback={<LoadingSpinner />}>
        <QASection />
      </Suspense>
    </div>
  )
}