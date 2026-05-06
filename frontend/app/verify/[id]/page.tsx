'use client'
import { useState } from 'react'
import { useParams } from 'next/navigation'
import { useJudgment } from '../../../hooks/useJudgment'
import PDFViewer from '../../../components/PDFViewer'
import FieldReview from '../../../components/FieldReview'
import AppealWindow from '../../../components/AppealWindow'
import type { ActionItem } from '../../../types/action'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const STATUS_STEPS = ['extracting','ocr','classifying','llm','enriching','ready']
const STATUS_LABELS: Record<string,string> = {
  pending: 'Starting...', extracting: 'Extracting text from PDF...',
  ocr: 'Running OCR on scanned pages...', classifying: 'Finding ORDER section...',
  llm: 'AI extracting directives (Gemini)...', enriching: 'Calculating deadlines & contempt risk...',
  ready: 'Complete ✅', failed: 'Failed ❌'
}

export default function VerifyPage() {
  const params = useParams()
  const id = params?.id as string
  const { status, progress, data, error } = useJudgment(id)
  const [selectedAction, setSelectedAction] = useState<ActionItem | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  if (error) return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center">
      <div className="text-5xl mb-4">❌</div>
      <h2 className="text-xl font-semibold text-slate-800 mb-2">Processing Failed</h2>
      <p className="text-slate-500">{error}</p>
    </div>
  )

  if (status !== 'ready') return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center">
      <div className="animate-spin w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-6" />
      <h2 className="text-xl font-semibold text-slate-800 mb-2">{STATUS_LABELS[status] || 'Processing...'}</h2>
      <div className="w-full bg-slate-200 rounded-full h-3 mb-2">
        <div className="bg-orange-500 h-3 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
      </div>
      <p className="text-sm text-slate-500">{progress}% complete</p>
      <div className="flex justify-center gap-1 mt-4">
        {STATUS_STEPS.map((s,i) => (
          <div key={s} className={`h-1.5 w-8 rounded-full ${
            STATUS_STEPS.indexOf(status) >= i ? 'bg-orange-500' : 'bg-slate-200'
          }`} />
        ))}
      </div>
    </div>
  )

  if (!data) return null

  const pdfUrl = data.pdf_url
    ? `${API_URL}${data.pdf_url}`
    : `${API_URL}/judgments/${id}/file`

  const sortedActions = [...(data.action_items || [])].sort((a, b) => (a.days_left ?? 999) - (b.days_left ?? 999))

  return (
    <div className="flex flex-col h-[calc(100vh-56px)]">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between">
        <div>
          <h2 className="font-semibold text-slate-800">{data.case_number || 'Judgment'}</h2>
          <p className="text-xs text-slate-500">
            {data.total_pages} pages · {data.action_items?.length || 0} directives extracted
            {data.has_kannada === 'true' && ' · ⚠️ Kannada pages — manual review recommended'}
          </p>
        </div>
        <a href="/dashboard" className="text-sm bg-orange-500 text-white px-3 py-1.5 rounded-lg hover:bg-orange-600">
          View Dashboard →
        </a>
      </div>

      {/* Split pane */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: PDF viewer */}
        <div className="w-1/2 border-r border-slate-200 overflow-hidden flex flex-col">
          <PDFViewer
            pdfUrl={pdfUrl}
            highlightPage={selectedAction?.source_page}
            highlightBbox={selectedAction?.source_bbox ? JSON.parse(selectedAction.source_bbox) : null}
          />
        </div>

        {/* Right: Field review */}
        <div className="w-1/2 overflow-y-auto p-4 bg-slate-50">
          <div className="mb-4">
            <h3 className="font-semibold text-slate-800 mb-1">Extracted Directives</h3>
            <p className="text-xs text-slate-500">Click any directive to highlight its source in the PDF →</p>
          </div>

          {sortedActions.length === 0 && (
            <div className="text-center py-8 text-slate-400">
              <p>No directives found in this judgment.</p>
              <p className="text-xs mt-1">Try uploading a judgment with an ORDER section containing "shall" or "directed to".</p>
            </div>
          )}

          {sortedActions.map(action => (
            <FieldReview
              key={`${action.id}-${refreshKey}`}
              action={action}
              onFieldClick={setSelectedAction}
              onUpdated={() => setRefreshKey(k => k + 1)}
              isSelected={selectedAction?.id === action.id}
            />
          ))}

          {data.appeal_windows?.length > 0 && (
            <div className="mt-4">
              <AppealWindow windows={data.appeal_windows} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
