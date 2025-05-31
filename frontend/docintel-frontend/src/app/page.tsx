import Link from 'next/link'

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto py-16 px-4 sm:px-6 lg:px-8 text-center">
      <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
        <span className="block">Document Intelligence</span>
        <span className="block text-primary-600">AI-Powered Insights</span>
      </h1>
      <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
        Upload your documents and get intelligent answers powered by AI. Extract knowledge from PDFs, Word documents, and more.
      </p>
      <div className="mt-10 flex justify-center space-x-4">
        <Link
          href="/upload"
          className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          Upload Document
        </Link>
        <Link
          href="/dashboard"
          className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200"
        >
          View Documents
        </Link>
      </div>
    </div>
  )
}