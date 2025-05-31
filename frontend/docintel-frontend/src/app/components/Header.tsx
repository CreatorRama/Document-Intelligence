import Link from 'next/link'

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-primary-600">
          Document Intelligence
        </Link>
        <nav className="flex space-x-6">
          <Link href="/dashboard" className="text-gray-600 hover:text-primary-600">
            Documents
          </Link>
          <Link href="/upload" className="text-gray-600 hover:text-primary-600">
            Upload
          </Link>
        </nav>
      </div>
    </header>
  )
}