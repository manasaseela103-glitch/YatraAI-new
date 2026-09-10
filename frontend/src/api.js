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
  plan: async (data) => {
    try {
      return await api('/trips/plan', { method: 'POST', body: JSON.stringify(data) })
    } catch (error) {
      console.warn('Backend unavailable, generating client-side fallback plan:', error)
      const interests = data.interests?.length ? data.interests : ['local highlights']
      const itinerary = []
      for (let day = 1; day <= (data.days || 3); day++) {
        const interest = interests[(day - 1) % interests.length]
        itinerary.push({
          day,
          morning: `Explore ${data.destination}'s ${interest} highlights`,
          afternoon: `Enjoy a ${(data.travel_style || data.style || 'cultural').toLowerCase()} experience in ${data.destination}`,
          evening: `Discover local food and night culture in ${data.destination}`,
        })
      }
      return {
        destination: data.destination,
        days: data.days || 3,
        travelers: data.travelers || 2,
        budget: data.budget || 25000,
        travel_style: data.travel_style || data.style || 'Cultural',
        interests: data.interests || [],
        itinerary,
        budget_breakdown: {
          accommodation: Math.round((data.budget || 25000) * 0.4),
          food: Math.round((data.budget || 25000) * 0.2),
          transport: Math.round((data.budget || 25000) * 0.15),
          activities: Math.round((data.budget || 25000) * 0.25),
        },
        ai_insight: `This ${data.days || 3}-day ${data.travel_style || 'Cultural'} plan for ${data.destination} is tailored around your interests.`,
        places: [],
      }
    }
  },
  generate: (data) => api('/trips/generate', { method: 'POST', body: JSON.stringify(data) }),
  replan: (data) => api('/trips/replan', { method: 'POST', body: JSON.stringify(data) }),
  accept: (id, data) => api(`/trips/${id}/accept-replan`, { method: 'PUT', body: JSON.stringify(data) }),
}
