'use client'

import { useState } from 'react'
import { uploadDocument } from '../../api/client'
import { useDropzone } from 'react-dropzone'
import { FiUpload, FiFile, FiX } from 'react-icons/fi'
import toast from 'react-hot-toast'
import LoadingSpinner from '../../components/LoadingSpinner'

interface UploadFormProps {
  onSuccess: () => void
}

export default function UploadForm({ onSuccess }: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0])
    },
  })

  const removeFile = () => {
    setFile(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setIsUploading(true)
    try {
      const response = await uploadDocument(file)
      console.log('Upload response:', response) // Debug log
      
      toast.success('Document uploaded successfully!')
      
      // Call onSuccess after successful upload
      onSuccess()
      
    } catch (error) {
      console.error('Upload error:', error) // Debug log
      toast.error('Failed to upload document. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-500'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-2">
          <FiUpload className="h-8 w-8 text-gray-400" />
          <p className="text-sm text-gray-600">
            {isDragActive
              ? 'Drop the file here'
              : 'Drag and drop a file here, or click to select'}
          </p>
          <p className="text-xs text-gray-500">PDF, DOCX, or TXT (Max 10MB)</p>
        </div>
      </div>

      {file && (
        <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <FiFile className="h-5 w-5 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">{file.name}</span>
            <span className="text-xs text-gray-500">{formatBytes(file.size)}</span>
          </div>
          <button
            type="button"
            onClick={removeFile}
            className="text-gray-400 hover:text-red-600"
          >
            <FiX className="h-5 w-5" />
          </button>
        </div>
      )}

      <button
        type="submit"
        disabled={!file || isUploading}
        className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        {isUploading ? <LoadingSpinner /> : 'Upload Document'}
      </button>
    </form>
  )
}

function formatBytes(bytes: number, decimals = 2) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}