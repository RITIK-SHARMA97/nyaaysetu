import UploadZone from '../components/UploadZone'

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 bg-orange-100 text-orange-800 text-xs font-medium px-3 py-1 rounded-full mb-4">
          🏆 AI for Bharat 2026 · Shortlisted
        </div>
        <h1 className="text-4xl font-bold text-slate-900 mb-4">
          NyaaySetu
        </h1>
        <p className="text-xl text-slate-600 mb-2">
          From Court Judgments to Verified Action Plans — in minutes.
        </p>
        <p className="text-sm text-slate-500 max-w-2xl mx-auto">
          Every AI legal tool in India was built for judges inside the court.
          NyaaySetu is the first system built for the <strong>government officer on the other side of the judgment</strong> — the one who must comply or face contempt.
        </p>
      </div>

      {/* Upload */}
      <UploadZone />

      {/* Demo notice */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl text-sm text-blue-800">
        <strong>Demo:</strong> No judgment PDF? Go to{' '}
        <a href="/dashboard" className="underline font-medium">Dashboard</a> to see pre-loaded Karnataka HC cases, or{' '}
        <a href="/briefing" className="underline font-medium">Briefing</a> for the new officer experience.
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mt-10">
        {[
          { val: '25+', label: 'Unique factors', sub: 'No competitor matches' },
          { val: '3', label: 'Departments tracked', sub: 'in demo data' },
          { val: '₹0', label: 'Infrastructure cost', sub: 'Fully open source stack' },
        ].map(s => (
          <div key={s.val} className="text-center p-4 bg-white border border-slate-200 rounded-xl shadow-sm">
            <div className="text-3xl font-bold text-orange-500">{s.val}</div>
            <div className="text-sm font-medium text-slate-700 mt-1">{s.label}</div>
            <div className="text-xs text-slate-400">{s.sub}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
