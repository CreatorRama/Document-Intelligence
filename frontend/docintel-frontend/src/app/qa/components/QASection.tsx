'use client'

import { useState } from 'react'
import { askQuestion } from '../../api/client'
import { QuestionResponse } from '../../lib/types'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'
import { useSearchParams } from 'next/navigation'

export default function QASection() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState<QuestionResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [documentError, setDocumentError] = useState(false)

  const searchParams = useSearchParams()
  const documentId = searchParams.get('documentId')

  if (!documentId) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No document selected. Please go back and select a document.</p>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setIsLoading(true)
    try {
      const data = await askQuestion(documentId, question)
      setResponse(data)
      setDocumentError(false)
    } catch (error) {
      toast.error('Failed to get answer. Please try again.')
      console.error(error)
      setDocumentError(true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {documentError && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <p className="text-red-700">Error connecting to document. Please check if the document still exists.</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-sm font-medium text-gray-700">
            Ask a question about this document
          </label>
          <div className="mt-1 flex rounded-md shadow-sm">
            <input
              type="text"
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex-1 min-w-0 block w-full px-3 py-2 rounded-l-md border-gray-300 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="Enter your question..."
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !question.trim()}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isLoading ? <LoadingSpinner /> : 'Ask'}
            </button>
          </div>
        </div>
      </form>

      {response && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Answer</h3>
            <p className="text-gray-700">{response.answer}</p>
          </div>
        </div>
      )}
    </div>
  )
}