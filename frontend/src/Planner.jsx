import { useState } from 'react'
import PlannerNav from './PlannerNav.jsx'
import { tripApi } from './api.js'

const travelStyles = ['Relaxed', 'Adventure', 'Family', 'Romantic', 'Cultural', 'Budget']
const interestOptions = ['Nature', 'History', 'Food', 'Culture', 'Adventure', 'Shopping', 'Photography', 'Spiritual']

function Field({ label, error, children }) {
  return <label className="planner-field"><span>{label}</span>{children}{error && <small className="field-error">{error}</small>}</label>
}

function Planner({ onNavigate }) {
  const [form, setForm] = useState({ destination: '', dates: '', days: '', travelers: '2', budget: '', style: '', interests: [] })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const updateField = (field, value) => setForm((current) => ({ ...current, [field]: value }))
  const toggleInterest = (interest) => updateField('interests', form.interests.includes(interest) ? form.interests.filter((item) => item !== interest) : [...form.interests, interest])

  const generateTrip = async (event) => {
    event.preventDefault()
    const nextErrors = {}
    if (!form.destination.trim()) nextErrors.destination = 'Where would you like to go?'
    if (!form.dates) nextErrors.dates = 'Choose your travel dates.'
    if (!form.days || Number(form.days) < 1) nextErrors.days = 'Add at least one day.'
    if (!form.travelers || Number(form.travelers) < 1) nextErrors.travelers = 'Add at least one traveler.'
    if (!form.budget || Number(form.budget) < 1) nextErrors.budget = 'Add your approximate budget.'
    if (!form.style) nextErrors.style = 'Choose a travel style.'
    if (!form.interests.length) nextErrors.interests = 'Choose at least one interest.'
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length) return
    setLoading(true)
    try {
      const trip = await tripApi.plan({ destination: form.destination.trim(), days: Number(form.days), travelers: Number(form.travelers), budget: Number(form.budget), travel_style: form.style, interests: form.interests })
      onNavigate('/itinerary', trip)
    } catch (error) {
      setErrors({ destination: error.message || 'We could not generate your trip. Please try again.' })
    } finally {
      setLoading(false)
    }
  }

  return <main className="planner-page"><PlannerNav /><section className="planner-wrap"><div className="planner-intro"><p className="eyebrow"><span></span> The good part starts now</p><h1>Design a trip<br /><em>that feels like you.</em></h1><p>Tell us a little about what you are looking for. We will shape the first draft of something wonderful.</p><div className="planner-progress"><span className="progress-active">01</span><span></span><span>02</span><span></span><span>03</span><small>Your preferences</small></div></div><form className="planner-form" onSubmit={generateTrip} noValidate><div className="form-heading"><span>Let’s get to know your journey</span><strong>01 / 03</strong></div><div className="form-grid"><Field label="Where are you going?" error={errors.destination}><input type="text" placeholder="e.g. Jaipur, Kyoto, or anywhere..." value={form.destination} onChange={(event) => updateField('destination', event.target.value)} /></Field><Field label="When are you travelling?" error={errors.dates}><input type="date" value={form.dates} onChange={(event) => updateField('dates', event.target.value)} /></Field><Field label="How many days?" error={errors.days}><input type="number" min="1" placeholder="7" value={form.days} onChange={(event) => updateField('days', event.target.value)} /></Field><Field label="How many travellers?" error={errors.travelers}><input type="number" min="1" placeholder="2" value={form.travelers} onChange={(event) => updateField('travelers', event.target.value)} /></Field><Field label="Your approximate budget (INR)" error={errors.budget}><div className="input-prefix"><span>₹</span><input type="number" min="1" placeholder="1,00,000" value={form.budget} onChange={(event) => updateField('budget', event.target.value)} /></div></Field></div><fieldset className="choice-group"><legend>What is your travel style?</legend><div className="choice-grid">{travelStyles.map((style) => <button className={form.style === style ? 'choice selected' : 'choice'} type="button" key={style} onClick={() => updateField('style', style)}>{style}<span>{form.style === style ? '✓' : '+'}</span></button>)}</div>{errors.style && <small className="field-error">{errors.style}</small>}</fieldset><fieldset className="choice-group"><legend>What are you curious about?</legend><div className="interest-grid">{interestOptions.map((interest) => <button className={form.interests.includes(interest) ? 'interest selected' : 'interest'} type="button" key={interest} onClick={() => toggleInterest(interest)}>{interest}</button>)}</div>{errors.interests && <small className="field-error">{errors.interests}</small>}</fieldset><div className="form-submit"><p>We use your answers to make the journey feel personal.</p><button className="primary-button generate-button" type="submit" disabled={loading}>{loading ? <><span className="loading-dots"><i></i><i></i><i></i></span> YatraAI is designing your journey...</> : <>Generate AI Trip <span aria-hidden="true">↗</span></>}</button></div></form></section></main>
}

export default Planner
