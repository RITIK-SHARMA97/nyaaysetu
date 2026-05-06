import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use(cfg => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('nyaaysetu_token')
    if (token) cfg.headers.Authorization = `Bearer ${token}`
  }
  return cfg
})

export const uploadJudgment = (file: File) => {
  const fd = new FormData()
  fd.append('file', file)
  return api.post('/judgments/upload', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const getJudgmentStatus = (id: string) => api.get(`/judgments/${id}/status`)
export const getJudgment = (id: string) => api.get(`/judgments/${id}`)
export const listJudgments = () => api.get('/judgments/')
export const patchAction = (id: string, data: object) => api.patch(`/actions/${id}`, data)
export const patchActionStatus = (id: string, status: string, notes?: string) =>
  api.patch(`/actions/${id}/status`, { status, notes })
export const getAction = (id: string) => api.get(`/actions/${id}`)
export const getAffidavit = (id: string) => api.get(`/actions/${id}/affidavit`)
export const getDashboard = () => api.get('/dashboard/summary')
export const getDashboardActions = (page = 1, status?: string, risk?: string) =>
  api.get('/dashboard/actions', { params: { page, status, risk } })
export const getBriefing = () => api.get('/officers/briefing')
export const getMe = () => api.get('/officers/me')
export const login = (email: string) => api.post('/auth/login', { email })
export const listDemoUsers = () => api.get('/auth/users')

export default api
