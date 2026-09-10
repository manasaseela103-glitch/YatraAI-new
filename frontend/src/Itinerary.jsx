import { useState } from 'react'
import PlannerNav from './PlannerNav.jsx'

const fallbackTrip = { destination: 'your destination', dates: '', days: 3, travelers: 2, budget: 0, travel_style: 'Curious', interests: [], itinerary: [], budget_breakdown: {} }
const money = (value) => `₹${Number(value || 0).toLocaleString('en-IN')}`

const normalizeItinerary = (itinerary, destination, places = []) => itinerary.map((item, dayIndex) => {
  const morningPlace = places[dayIndex * 3]
  const afternoonPlace = places[dayIndex * 3 + 1]
  const eveningPlace = places[dayIndex * 3 + 2]
  return {
    label: `Day ${item.day}`,
    date: `Day ${item.day}`,
    activities: [
      { time: 'Morning', place: morningPlace?.name || destination, activity: item.morning, description: item.morning, cost: 'Included', travel: 'Flexible', recommendation: item.morning, placeData: morningPlace, lat: morningPlace?.latitude, lng: morningPlace?.longitude },
      { time: 'Afternoon', place: afternoonPlace?.name || destination, activity: item.afternoon, description: item.afternoon, cost: 'Included', travel: 'Flexible', recommendation: item.afternoon, placeData: afternoonPlace, lat: afternoonPlace?.latitude, lng: afternoonPlace?.longitude },
      { time: 'Evening', place: eveningPlace?.name || destination, activity: item.evening, description: item.evening, cost: 'Included', travel: 'Flexible', recommendation: item.evening, placeData: eveningPlace, lat: eveningPlace?.latitude, lng: eveningPlace?.longitude },
    ],
  }
})

function Activity({ item, index }) {
  const place = item.placeData
  const mapsSearchUrl = place?.google_maps_url || (item.lat && item.lng ? `https://www.google.com/maps/search/?api=1&query=${item.lat},${item.lng}` : (item.place ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(item.place)}` : null))
  const mapsDirectionsUrl = place?.directions_url || (item.lat && item.lng ? `https://www.google.com/maps/dir/?api=1&destination=${item.lat},${item.lng}` : (item.place ? `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(item.place)}` : null))

  return (
    <article className="timeline-item" style={{ '--delay': `${index * 80}ms` }}>
      <div className="timeline-time">{item.time}</div>
      <div className="timeline-line"><span></span></div>
      <div className="activity-card">
        <div className="activity-top">
          <div>
            <span className="activity-place">{item.place}</span>
            <h3>{item.activity}</h3>
          </div>
          <span className="activity-index">0{index + 1}</span>
        </div>
        <p>{item.description}</p>
        <div className="activity-meta">
          <span>Cost <strong>{item.cost}</strong></span>
          <span>Travel <strong>{item.travel}</strong></span>
        </div>
        <div className="recommendation">
          <span>✦</span>
          <div>
            <b>AI Recommendation</b>
            <p>{item.recommendation}</p>
          </div>
        </div>
        {place && (
          <div className="activity-place-data">
            <strong>{place.name}</strong>
            {place.rating && <span>★ {place.rating}</span>}
            {place.address && <small>{place.address}</small>}
            {place.opening_hours?.[0] && <small>{place.opening_hours[0]}</small>}
            <div className="activity-place-links">
              {place.google_maps_url && <a href={place.google_maps_url} target="_blank" rel="noreferrer">View on Maps ↗</a>}
              {place.directions_url && <a href={place.directions_url} target="_blank" rel="noreferrer">Directions ↗</a>}
            </div>
          </div>
        )}
        {!place && (mapsSearchUrl || mapsDirectionsUrl) && (
          <div className="activity-map-actions">
            {mapsSearchUrl && <a className="text-link" target="_blank" rel="noreferrer" href={mapsSearchUrl}>Open map ↗</a>}
            {mapsDirectionsUrl && <a className="text-link" target="_blank" rel="noreferrer" href={mapsDirectionsUrl}>Directions ↗</a>}
          </div>
        )}
      </div>
    </article>
  )
}

function Itinerary({ tripData, onNavigate }) {
  const [activeDay, setActiveDay] = useState(0)
  const trip = tripData ? { ...tripData, style: tripData.travel_style || tripData.style, interests: tripData.interests || [] } : fallbackTrip
  const days = trip.days_plan?.length ? trip.days_plan : normalizeItinerary(trip.itinerary || [], trip.destination, trip.places)
  const day = days[Math.min(activeDay, Math.max(0, days.length - 1))]
  const breakdown = trip.budget_breakdown || {}
  return <main className="planner-page itinerary-page"><PlannerNav /><section className="itinerary-header"><div><p className="eyebrow"><span></span> Your journey, thoughtfully mapped</p><h1>Your AI-Powered<br /><em>Trip Plan</em></h1><p className="itinerary-lede">A live itinerary shaped around your interests, timing and budget.</p></div><div className="trip-meta">Generated just now <span>•</span> {trip.destination}</div></section><section className="summary-grid"><div className="summary-card"><span>Destination</span><strong>{trip.destination}</strong><small>{trip.style} travel</small></div><div className="summary-card"><span>Duration</span><strong>{trip.days} days</strong><small>{trip.dates || 'Dates flexible'}</small></div><div className="summary-card"><span>Travellers</span><strong>{trip.travelers} people</strong><small>{trip.interests.join(', ') || 'Personalised plan'}</small></div><div className="summary-card"><span>Est. budget</span><strong>{money(trip.total_estimated_cost || trip.budget)}</strong><small>{money((trip.budget || 0) / Math.max(1, trip.travelers))} per person</small></div></section><section className="itinerary-content" id="daily-itinerary"><div className="section-title-row"><div><p className="section-kicker">Daily itinerary</p><h2>Take it <em>day by day.</em></h2></div><span className="route-status"><i></i> Optimised for your rhythm</span></div>{days.length ? <><div className="day-tabs" role="tablist">{days.map((item, index) => <button key={item.label} className={activeDay === index ? 'day-tab active' : 'day-tab'} type="button" onClick={() => setActiveDay(index)}><strong>{item.label}</strong><span>{item.date}</span></button>)}</div><div className="timeline">{day.activities.map((item, index) => <Activity item={item} index={index} key={`${item.place}-${index}`} />)}</div></> : <p className="field-error">No itinerary is loaded. Start planning a trip first.</p>}</section><section className="insight-card"><div className="insight-icon">✦</div><div><p className="section-kicker">A little guidance from YatraAI</p><h2>AI Travel Insight</h2><p>{trip.ai_insight || 'Your trip will be paced to balance landmark moments with flexible local discovery.'}</p></div></section><section className="budget-section" id="budget-summary"><div className="budget-heading"><p className="section-kicker">Keep an eye on the big picture</p><h2>Budget <em>summary.</em></h2></div><div className="budget-card">{[['Accommodation', breakdown.accommodation, 38], ['Food', breakdown.food, 22], ['Transport', breakdown.transport, 16], ['Activities', breakdown.activities, 24]].map(([label, value, width]) => <div className="budget-row" key={label}><span>{label}</span><strong>{money(value)}</strong><i><b style={{ width: `${width}%` }}></b></i></div>)}<div className="budget-total"><span>Total estimated</span><strong>{money(breakdown.total || trip.budget)}</strong></div></div></section><section className="action-row"><button className="primary-button" type="button" onClick={() => onNavigate('/adaptive', trip)}>Re-plan My Trip ↗</button><a className="secondary-button" href="/budget">Optimize Budget ↗</a></section></main>
}

export default Itinerary
