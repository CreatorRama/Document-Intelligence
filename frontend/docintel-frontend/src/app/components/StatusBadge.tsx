import { STATUS_COLORS } from '../lib/constants'

interface StatusBadgeProps {
  status: 'processing' | 'completed' | 'failed' | 'processed' | 'uploading' | string
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  // Handle null, undefined, or invalid status values
  if (!status || typeof status !== 'string') {
    status = 'unknown'
  }

  // Map backend status values to frontend status values
  const normalizeStatus = (backendStatus: string): keyof typeof STATUS_COLORS => {
    const normalized = backendStatus.toLowerCase()
    
    switch (normalized) {
      case 'processed':
        return 'completed'
      case 'processing':
      case 'uploading':
        return 'processing'
      case 'failed':
      case 'error':
        return 'failed'
      default:
        // If status exists in STATUS_COLORS, use it; otherwise default to 'processing'
        return (normalized in STATUS_COLORS) ? normalized as keyof typeof STATUS_COLORS : 'processing'
    }
  }

  const normalizedStatus = normalizeStatus(status)
  const displayStatus = status.charAt(0).toUpperCase() + status.slice(1).toLowerCase()

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${STATUS_COLORS[normalizedStatus] || STATUS_COLORS.processing}`}>
      {displayStatus}
    </span>
  )
}