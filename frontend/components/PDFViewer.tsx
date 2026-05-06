'use client'
import { useEffect, useRef, useState } from 'react'

interface Props {
  pdfUrl: string
  highlightPage?: number
  highlightBbox?: number[] | null
}

export default function PDFViewer({ pdfUrl, highlightPage, highlightBbox }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const renderTaskRef = useRef<any>(null)
  const renderSequenceRef = useRef(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [pdfDoc, setPdfDoc] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [scale, setScale] = useState(1.2)

  useEffect(() => {
    if (!pdfUrl) return
    loadPDF()
  }, [pdfUrl])

  useEffect(() => {
    if (highlightPage && highlightPage !== currentPage) {
      setCurrentPage(highlightPage)
    }
  }, [highlightPage])

  useEffect(() => {
    if (!pdfDoc) return
    const renderId = ++renderSequenceRef.current
    renderPage(currentPage, renderId)

    return () => {
      if (renderTaskRef.current) {
        renderTaskRef.current.cancel()
        renderTaskRef.current = null
      }
    }
  }, [pdfDoc, currentPage, scale, highlightBbox, highlightPage])

  const loadPDF = async () => {
    try {
      setLoading(true)
      setError(null)
      const pdfjsLib = await import('pdfjs-dist')
      pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'
      const doc = await pdfjsLib.getDocument(pdfUrl).promise
      setPdfDoc(doc)
      setTotalPages(doc.numPages)
      setLoading(false)
    } catch (e) {
      console.error('Failed to load PDF preview', e)
      setError('Could not load PDF. The file may not be accessible.')
      setLoading(false)
    }
  }

  const renderPage = async (pageNum: number, renderId: number) => {
    if (!pdfDoc || !canvasRef.current) return

    if (renderTaskRef.current) {
      renderTaskRef.current.cancel()
      renderTaskRef.current = null
    }

    const page = await pdfDoc.getPage(pageNum)
    if (renderId !== renderSequenceRef.current || !canvasRef.current) return

    const viewport = page.getViewport({ scale })
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')!
    canvas.width = viewport.width
    canvas.height = viewport.height

    const renderTask = page.render({ canvasContext: ctx, viewport })
    renderTaskRef.current = renderTask

    try {
      await renderTask.promise
    } catch (e: any) {
      if (e?.name === 'RenderingCancelledException') return
      throw e
    } finally {
      if (renderTaskRef.current === renderTask) {
        renderTaskRef.current = null
      }
    }

    if (renderId !== renderSequenceRef.current) return

    // Draw highlight if bbox provided and on correct page
    if (highlightBbox && highlightPage === pageNum && highlightBbox.length === 4) {
      const [x0, y0, x1, y1] = highlightBbox
      ctx.fillStyle = 'rgba(255, 200, 0, 0.4)'
      ctx.strokeStyle = 'rgba(255, 150, 0, 0.8)'
      ctx.lineWidth = 2
      const scaledX = x0 * scale
      const scaledY = y0 * scale
      const scaledW = (x1 - x0) * scale
      const scaledH = (y1 - y0) * scale
      ctx.fillRect(scaledX, scaledY, scaledW, scaledH)
      ctx.strokeRect(scaledX, scaledY, scaledW, scaledH)
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-96 bg-slate-100 rounded-xl">
      <div className="text-center">
        <div className="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-3" />
        <p className="text-sm text-slate-600">Loading PDF...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="flex items-center justify-center h-96 bg-red-50 rounded-xl border border-red-200">
      <div className="text-center p-6">
        <p className="text-red-600 font-medium mb-2">PDF Preview Unavailable</p>
        <p className="text-sm text-red-500">{error}</p>
        <a href={pdfUrl} target="_blank" rel="noreferrer" className="mt-3 inline-block text-sm text-orange-600 hover:underline">
          Open PDF directly
        </a>
        <p className="text-xs text-slate-500 mt-2">The extracted directives are shown on the right →</p>
      </div>
    </div>
  )

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="flex items-center justify-between p-3 bg-slate-800 rounded-t-xl text-white text-sm">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage <= 1}
            className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 disabled:opacity-40"
          >←</button>
          <span>Page {currentPage} / {totalPages}</span>
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages}
            className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 disabled:opacity-40"
          >→</button>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => setScale(s => Math.max(0.5, s - 0.2))} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600">−</button>
          <span>{Math.round(scale * 100)}%</span>
          <button onClick={() => setScale(s => Math.min(3, s + 0.2))} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600">+</button>
        </div>
      </div>
      {/* Canvas */}
      <div className="overflow-auto flex-1 bg-slate-600 p-4">
        <canvas ref={canvasRef} className="mx-auto shadow-xl" />
      </div>
      {highlightBbox && (
        <div className="p-2 bg-yellow-50 border-t border-yellow-200 text-xs text-yellow-800 text-center">
          🔍 Source sentence highlighted in yellow
        </div>
      )}
    </div>
  )
}
