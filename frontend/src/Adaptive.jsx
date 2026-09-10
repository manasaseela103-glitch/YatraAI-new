import { useState } from 'react'
import PlannerNav from './PlannerNav.jsx'
import { tripApi } from './api.js'

const scenarios = [
  { id: 'attraction_closed', label: 'Attraction Closed' },
  { id: 'bad_weather', label: 'Bad Weather' },
  { id: 'heavy_crowd', label: 'Heavy Crowd' },
  { id: 'transport_delay', label: 'Transport Delay' },
  { id: 'budget_exceeded', label: 'Budget Exceeded' },
]

const fallbackTrip = { destination: 'your destination', days: 0, travelers: 0, budget: 0, interests: [], itinerary: [], days_plan: [] }

function getCurrentActivity(trip) {
  const firstDay = trip.itinerary?.[0]
  if (firstDay) return { time: 'Morning', place: trip.destination, activity: firstDay.morning, description: firstDay.morning, cost: 'Included', travel: 'Flexible' }
  return trip.days_plan?.[0]?.activities?.[0] || { place: 'Scheduled attraction', activity: 'Current plan', time: 'Morning', cost: 'Included', travel: 'Flexible' }
}

function getUpdatedPreview(itinerary, destination, places = []) {
  const firstDay = itinerary?.[0]
  if (!firstDay) return null
  const place = places[0]
  if (firstDay.morning) return { time: 'Morning', activity: firstDay.morning, place: <>{destination}{place && <span className="adaptive-place-data"> · {place.name}{place.rating && ` · ★ ${place.rating}`}{place.address && ` · ${place.address}`}{place.opening_hours?.[0] && ` · ${place.opening_hours[0]}`} {place.google_maps_url && <a href={place.google_maps_url} target="_blank" rel="noreferrer">Maps ↗</a>} {place.directions_url && <a href={place.directions_url} target="_blank" rel="noreferrer">Directions ↗</a>}</span>}</> }
  return firstDay.activities?.[0] || null
}

function Adaptive({ tripData, onNavigate }) {
  const trip = tripData || fallbackTrip
  const [scenario, setScenario] = useState(scenarios[0])
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [accepted, setAccepted] = useState(false)
  const current = getCurrentActivity(trip)
  const currentItinerary = trip.itinerary?.length ? trip.itinerary : trip.days_plan || []
  const updatedPreview = getUpdatedPreview(recommendation?.updated_itinerary, trip.destination, recommendation?.recommended_places)

  const requestPlan = async (nextScenario) => {
    setScenario(nextScenario)
    setLoading(true)
    setError('')
    setAccepted(false)
    try {
      const response = await tripApi.replan({ current_itinerary: currentItinerary, scenario: nextScenario.id, destination: trip.destination, budget: trip.budget })
      setRecommendation(response)
    } catch (err) {
      setError(err.message || 'We could not re-plan this trip. Please try again.')
      setRecommendation(null)
    } finally {
      setLoading(false)
    }
  }

  const accept = () => {
    if (!recommendation) return
    const updated = { ...trip, itinerary: recommendation.updated_itinerary, places: recommendation.recommended_places || trip.places || [] }
    if (trip.days_plan?.length) updated.days_plan = recommendation.updated_itinerary
    setAccepted(true)
    window.setTimeout(() => onNavigate('/itinerary', updated), 700)
  }

  return <main className="planner-page adaptive-page"><PlannerNav /><section className="adaptive-demo-header"><div><p className="eyebrow"><span></span> YatraAI adaptive intelligence</p><h1>Adaptive AI<br /><em>Re-planner</em></h1><p>Plans change. Your journey does not have to.</p></div><div className="adaptive-trip-context"><span>Your active trip</span><strong>{trip.destination}</strong><small>{trip.days} days • {trip.travelers} travellers • ₹{Number(trip.budget).toLocaleString('en-IN')}</small></div></section><section className="scenario-selector"><div className="section-title-row"><div><p className="section-kicker">Simulate a disruption</p><h2>What changed?</h2></div><span className="live-indicator"><i></i> Live API</span></div><div className="scenario-buttons">{scenarios.map((item, index) => <button key={item.id} className={scenario.id === item.id ? 'scenario-button active' : 'scenario-button'} type="button" onClick={() => requestPlan(item)}><span>0{index + 1}</span>{item.label}</button>)}</div></section><section className="adaptive-itinerary-grid"><div className="current-plan"><div className="adaptive-label">CURRENT PLAN <span>{current.time}</span></div><div className="current-activity"><div className="timeline-dot"></div><div><span>{current.place}</span><h2>{current.activity}</h2><p>{current.description || 'Your scheduled experience.'}</p><div className="activity-meta"><span>Cost <strong>{current.cost}</strong></span><span>Travel <strong>{current.travel}</strong></span></div></div></div></div><div className="travel-alert"><div className="alert-icon">!</div><div><span>PROBLEM</span><h2>{recommendation?.alert || (error ? 'Unable to check this scenario' : 'Select a disruption')}</h2><small>Scenario: {scenario.label}</small></div></div></section><section className="recommendation-section"><div className="processing-state"><div className="ai-orbit"><span>✦</span></div><div><span className="adaptive-label">YatraAI PROCESSING</span><h2>{loading ? 'Finding the best alternative...' : 'AI Recommendation'}</h2><p>{error || recommendation?.ai_insight || (!loading && 'Matched to your available time, interests and budget.')}</p></div></div>{recommendation && !loading && <><div className="recommendation-card"><div className="recommendation-card-top"><div><span>AI RECOMMENDATION</span><h2>{recommendation.recommended_changes?.[0]}</h2></div><strong>↗</strong></div><div className="recommendation-details"><span><b>{recommendation.budget_impact?.summary || 'No budget change'}</b>Budget impact</span><span><b>{recommendation.updated_itinerary?.length || trip.days}</b>Days planned</span><span><b>{scenario.label}</b>Scenario</span></div><p>{recommendation.reason}</p></div>{updatedPreview && <div className="recommendation-card updated-plan-card"><div className="recommendation-card-top"><div><span>UPDATED PLAN</span><h2>{updatedPreview.activity}</h2></div><strong>✓</strong></div><p>{updatedPreview.place} • {updatedPreview.time}</p></div>}</>}</section>{accepted ? <section className="success-card"><div className="success-mark">✓</div><div><h2>Trip Updated Successfully</h2><p>Opening your updated itinerary...</p></div></section> : <section className="adaptive-actions"><button className="primary-button" type="button" disabled={loading || !recommendation} onClick={accept}>Accept New Plan ↗</button><button className="secondary-button" type="button" onClick={() => requestPlan(scenarios[(scenarios.findIndex((item) => item.id === scenario.id) + 1) % scenarios.length])}>View Other Alternatives ↗</button></section>}</main>
}

export default Adaptive
