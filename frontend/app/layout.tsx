import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NyaaySetu — Court Compliance Management',
  description: 'AI-powered court compliance management for Karnataka Government',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50">
        <nav className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between sticky top-0 z-50 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-sm">NS</div>
            <div>
              <span className="font-semibold text-slate-800">NyaaySetu</span>
              <span className="text-xs text-slate-500 ml-2">Karnataka Government · Court Compliance</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <a href="/" className="text-sm text-slate-600 hover:text-slate-900">Upload</a>
            <a href="/dashboard" className="text-sm text-slate-600 hover:text-slate-900">Dashboard</a>
            <a href="/briefing" className="text-sm text-slate-600 hover:text-slate-900">Briefing</a>
            <a href="/login" className="text-sm bg-orange-500 text-white px-3 py-1.5 rounded-lg hover:bg-orange-600">Login</a>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}
