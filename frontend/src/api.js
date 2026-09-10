const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function api(path, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options,
    })
    const payload = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(payload.detail || 'Something went wrong. Please try again.')
    return payload
  } catch (error) {
    if (error.name === 'TypeError' && (error.message.includes('fetch') || error.message.includes('NetworkError') || error.message.includes('Failed'))) {
      throw new Error('Unable to connect to YatraAI backend. Please ensure the Python backend server is running on http://127.0.0.1:8000 (run `uvicorn main:app --reload` inside the `backend` folder).')
    }
    throw error
  }
}

export const tripApi = {
  plan: (data) => api('/trips/plan', { method: 'POST', body: JSON.stringify(data) }),
  generate: (data) => api('/trips/generate', { method: 'POST', body: JSON.stringify(data) }),
  replan: (data) => api('/trips/replan', { method: 'POST', body: JSON.stringify(data) }),
  accept: (id, data) => api(`/trips/${id}/accept-replan`, { method: 'PUT', body: JSON.stringify(data) }),
}
