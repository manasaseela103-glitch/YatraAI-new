import { useEffect, useState } from 'react'
import PlannerNav from './PlannerNav.jsx'
import { destinations, experiences, gems } from './discoveryData.js'
import { api } from './api.js'

const destinationFilters = ['All', 'Popular', 'Nature', 'Culture', 'Food', 'Adventure', 'History']
const gemFilters = ['All', 'Low Crowd', 'Budget Friendly', 'Nature', 'Culture', 'Adventure']
const fallback = (event) => { event.currentTarget.style.display = 'none' }

function Image({ src, alt }) { return <div className="discovery-image"><img src={src} onError={fallback} alt={alt} /></div> }
function FilterBar({ filters, active, onChange }) { return <div className="discovery-filters" role="tablist">{filters.map((filter) => <button key={filter} type="button" className={active === filter ? 'filter active' : 'filter'} role="tab" aria-selected={active === filter} onClick={() => onChange(filter)}>{filter}</button>)}</div> }
function PageIntro({ kicker, title, emphasis, subtitle }) { return <section className="discovery-intro"><p className="eyebrow"><span></span> {kicker}</p><h1>{title}<br /><em>{emphasis}</em></h1><p>{subtitle}</p></section> }

function Explore() {
  const [filter, setFilter] = useState('All')
  const [items, setItems] = useState(destinations)
  useEffect(() => { api('/destinations').then(setItems).catch(() => {}) }, [])
  const visible = items.filter((item) => filter === 'All' || item.category === filter)
  return <main className="discovery-page"><PlannerNav /><PageIntro kicker="Curated for the curious" title="Explore Your Next" emphasis="Journey" subtitle="Discover popular destinations and experiences curated by YatraAI." /><section className="discovery-section"><FilterBar filters={destinationFilters} active={filter} onChange={setFilter} /><div className="destination-grid">{visible.map((item) => <article className="destination-tile" key={item.name}><Image src={item.image} alt={`${item.name} landscape`} /><div className="tile-body"><div className="tile-heading"><div><span>{item.region}</span><h2>{item.name}</h2></div><b>★ {item.rating}</b></div><p>{item.description}</p><div className="tile-meta"><span>From <strong>{item.budget}</strong></span><span className={`crowd ${item.crowd.toLowerCase()}`}>{item.crowd} crowd</span></div><a className="text-link" href={`#/explore/${item.name.toLowerCase().replaceAll(' ', '-')}`}>Explore <span>↗</span></a></div></article>)}</div></section><section className="recommendation-strip"><div><p className="section-kicker">A thoughtful starting point</p><h2>Recommended<br /><em>For You</em></h2></div><div className="recommendation-copy"><p>Based on the way you like to travel, we think you might enjoy places with room to breathe, a story around every corner and something delicious waiting at the end.</p><div><span>Slow travel</span><span>Culture seekers</span><span>Food lovers</span></div></div></section></main>
}

function HiddenGems() {
  const [filter, setFilter] = useState('All')
  const [items, setItems] = useState(gems)
  useEffect(() => { api('/gems').then(setItems).catch(() => {}) }, [])
  const visible = items.filter((item) => filter === 'All' || (filter === 'Low Crowd' && item.crowd.toLowerCase().includes('low')) || (filter === 'Budget Friendly' && Number(item.budget.replace(/\D/g, '')) < 16000) || item.tag === filter)
  return <main className="discovery-page gems-page"><PlannerNav /><PageIntro kicker="The road less travelled" title="Travel Beyond the" emphasis="Tourist Map" subtitle="Discover beautiful places away from overcrowded tourist hotspots." /><section className="discovery-section"><FilterBar filters={gemFilters} active={filter} onChange={setFilter} /><div className="gem-grid">{visible.map((item) => <article className="gem-tile" key={item.place}><Image src={item.image} alt={`${item.place} landscape`} /><div className="gem-body"><div className="tile-heading"><div><span>{item.location}</span><h2>{item.place}</h2></div><b className="low-crowd">● {item.crowd}</b></div><p>{item.why}</p><div className="gem-details"><span><small>Best time</small>{item.best}</span><span><small>From</small>{item.budget}</span><span><small>Local experience</small>{item.experience}</span></div><a className="text-link" href={`#/hidden-gems/${item.place.toLowerCase()}`}>Discover <span>↗</span></a></div></article>)}</div></section><section className="gem-insight"><div className="insight-icon">✦</div><div><p className="section-kicker">A quieter kind of intelligence</p><h2>YatraAI Hidden Gem Insight</h2><p>This destination receives fewer visitors than nearby popular attractions while offering a similar cultural experience.</p></div></section></main>
}

function Experiences() {
  const [filter, setFilter] = useState('All')
  const [items, setItems] = useState(experiences)
  useEffect(() => { api('/experiences').then(setItems).catch(() => {}) }, [])
  const filters = ['All', ...new Set(items.map((item) => item.type))]
  const visible = items.filter((item) => filter === 'All' || item.type === filter)
  return <main className="discovery-page experiences-page"><PlannerNav /><PageIntro kicker="Meet the people behind the place" title="Experience the" emphasis="Destination Like a Local" subtitle="Connect with local people, businesses and authentic experiences." /><section className="discovery-section"><FilterBar filters={filters} active={filter} onChange={setFilter} /><div className="experience-grid">{visible.map((item) => <article className="experience-tile" key={item.name}><Image src={item.image} alt={item.name} /><div className="experience-body"><span className="experience-type">{item.type}</span><h2>{item.name}</h2><p>{item.description}</p><div className="provider"><span>{item.provider}</span><small>{item.location}</small></div><div className="experience-meta"><b>★ {item.rating}</b><strong>{item.price}</strong></div><a className="text-link" href={`#/experiences/${item.name.toLowerCase().replaceAll(' ', '-')}`}>View Experience <span>↗</span></a></div></article>)}</div></section><section className="local-flow"><div><p className="section-kicker">The good travels further</p><h2>Support <em>Local Tourism.</em></h2><p>When you choose a local experience, your trip becomes more meaningful and your spending stays close to the people who make a place special.</p></div><div className="flow-diagram"><div><strong>Tourists</strong><span>discover + share</span></div><b>→</b><div><strong>Local Businesses</strong><span>earn + grow</span></div><b>→</b><div><strong>Local Economy</strong><span>thrive + continue</span></div></div></section></main>
}

export { Explore, HiddenGems, Experiences }
