'use client'

import UploadForm from './components/UploadForm'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function UploadPage() {
  const router = useRouter()

  const handleSuccess = () => {
    console.log('Upload success callback triggered') // Debug log
    
    // Add a small delay to ensure the upload is fully processed
    setTimeout(() => {
      console.log('Navigating to dashboard') // Debug log
      router.push('/dashboard')
    }, 100)
  }

  // Debug: Log when component mounts
  useEffect(() => {
    console.log('Upload page mounted')
  }, [])

  return (
    <div className="max-w-2xl mx-auto">
      <div className="space-y-8">
        <div className="space-y-2">
          <h1 className="text-2xl font-bold text-gray-900">Upload Document</h1>
          <p className="text-gray-600">
            Upload a PDF, Word, or Text document to process it with AI.
          </p>
        </div>

        <UploadForm onSuccess={handleSuccess} />
      </div>
    </div>
  )
}