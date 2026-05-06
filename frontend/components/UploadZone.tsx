'use client'
import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { uploadJudgment } from '../lib/api'

export default function UploadZone() {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const handleFile = async (file: File) => {
    if (!file.name.endsWith('.pdf')) { setError('Only PDF files accepted'); return }
    setUploading(true); setError(null)
    try {
      const res = await uploadJudgment(file)
      router.push(`/verify/${res.data.judgment_id}`)
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Upload failed. Is the backend running?')
      setUploading(false)
    }
  }

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault(); setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }, [])

  return (
    <div>
      <label
        className={`block border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
          dragging ? 'border-orange-400 bg-orange-50' : 'border-slate-300 bg-white hover:border-orange-300 hover:bg-orange-50'
        } ${uploading ? 'opacity-60 pointer-events-none' : ''}`}
        onDragOver={e => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
      >
        <input type="file" accept=".pdf" className="hidden" onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])} />
        {uploading ? (
          <div>
            <div className="animate-spin w-10 h-10 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-slate-600 font-medium">Uploading judgment...</p>
            <p className="text-sm text-slate-400 mt-1">AI processing will begin automatically</p>
          </div>
        ) : (
          <div>
            <div className="text-5xl mb-4">📄</div>
            <p className="text-lg font-semibold text-slate-700 mb-2">Drop Karnataka HC Judgment PDF</p>
            <p className="text-sm text-slate-500">or click to browse · PDF only · Max 50MB</p>
          </div>
        )}
      </label>
      {error && (
        <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">
          ❌ {error}
        </div>
      )}
    </div>
  )
}
