'use client'

import { useState } from 'react'
import { askQuestion } from '../../api/client'
import { QuestionResponse } from '../../lib/types'
import LoadingSpinner from '../../components/LoadingSpinner'
import toast from 'react-hot-toast'

interface QASectionProps {
  documentId: string
}

export default function QASection({ documentId }: QASectionProps) {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState<QuestionResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setIsLoading(true)
    try {
      const data = await askQuestion(documentId, question)
      console.log(data)
      setResponse(data)
    } catch (error) {
      toast.error('Failed to get answer. Please try again.')
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
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