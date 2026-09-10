import { useState } from 'react'
import './App.css'
import Planner from './Planner.jsx'
import Itinerary from './Itinerary.jsx'
import Adaptive from './Adaptive.jsx'
import { Explore, HiddenGems, Experiences } from './Discovery.jsx'
import { BusinessDashboard, AdminDashboard, BudgetPage, SafetyPage } from './DashboardViews.jsx'

function App() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [route, setRoute] = useState(window.location.pathname)
  const [tripData, setTripData] = useState(null)

  const navigate = (path, state = null) => {
    window.history.pushState(state, '', path)
    if (state) setTripData(state)
    setRoute(path)
  }

  if (route === '/planner') return <Planner onNavigate={navigate} />
  if (route === '/itinerary') return <Itinerary tripData={tripData} onNavigate={navigate} />
  if (route === '/adaptive') return <Adaptive tripData={tripData} onNavigate={navigate} />
  if (route === '/explore' || route.startsWith('/explore/')) return <Explore />
  if (route === '/hidden-gems' || route.startsWith('/hidden-gems/')) return <HiddenGems />
  if (route === '/experiences' || route.startsWith('/experiences/')) return <Experiences />
  if (route === '/business') return <BusinessDashboard />
  if (route === '/admin') return <AdminDashboard />
  if (route === '/budget') return <BudgetPage />
  if (route === '/safety') return <SafetyPage />

  const closeMenu = () => setMenuOpen(false)

  return (
    <main className="home-page">
      <nav className="nav-shell home-nav" aria-label="Main navigation">
        <a className="brand" href="#top" onClick={closeMenu}><span className="brand-mark">Y</span><span>Yatra<span className="brand-accent">AI</span></span></a>
        <button className="menu-toggle" type="button" aria-expanded={menuOpen} aria-controls="nav-links" onClick={() => setMenuOpen(!menuOpen)}><span className="sr-only">Toggle menu</span><span></span><span></span></button>
        <div className={`nav-links ${menuOpen ? 'is-open' : ''}`} id="nav-links">
          <a href="/" onClick={closeMenu}>Home</a><a href="/explore" onClick={closeMenu}>Explore</a><a href="/hidden-gems" onClick={closeMenu}>Hidden Gems</a><a href="/experiences" onClick={closeMenu}>Experiences</a><a href="/business" onClick={closeMenu}>Business</a><a href="/admin" onClick={closeMenu}>Admin</a><a className="nav-cta" href="/planner" onClick={closeMenu}>Plan My Trip <span aria-hidden="true">↗</span></a>
        </div>
      </nav>
      <section className="home-hero" id="top">
        <div className="home-hero-copy"><p className="home-eyebrow">AI-powered travel, beautifully planned</p><h1>Yatra<span>AI</span></h1><h2>Plan Smart.<br /><em>Travel Better.</em><br />Adapt Instantly.</h2><p className="home-hero-text">Your intelligent travel companion for thoughtful itineraries, hidden gems and calm decisions when plans change.</p><a className="home-cta" href="/planner">Plan My Trip <span aria-hidden="true">↗</span></a><div className="home-proof"><span>✦</span> Personalised in seconds <i></i><span>✦</span> Ready for change</div></div>
        <div className="home-visual" aria-label="AI travel planning visualization"><div className="visual-glow"></div><div className="travel-photo"><img src="https://images.unsplash.com/photo-1530789253388-582c481c54b0?auto=format&fit=crop&w=1100&q=85" onError={(event) => { event.currentTarget.style.display = 'none' }} alt="Traveler looking over a mountain valley" /><div className="photo-caption"><span>01</span><strong>Go somewhere<br />that feels like you.</strong></div></div><div className="ai-orbit-card"><span className="orbit-spark">✦</span><div><small>YatraAI intelligence</small><strong>Your next best move</strong></div><b>↗</b></div></div>
      </section>
      <section className="home-capabilities" id="about"><div className="home-section-heading"><p className="home-eyebrow">One intelligent companion</p><h2>Travel planning,<br /><em>with more feeling.</em></h2></div><div className="capability-grid"><a href="/planner" className="capability-card capability-primary"><span>01</span><div><strong>AI Trip Planner</strong><p>Build a day-by-day plan around your pace, people and passions.</p></div><b>↗</b></a><a href="/adaptive" className="capability-card"><span>02</span><div><strong>Adaptive Re-planning</strong><p>When life changes, get a smarter next step without the stress.</p></div><b>↗</b></a><a href="/hidden-gems" className="capability-card"><span>03</span><div><strong>Hidden Gems</strong><p>Find local places and small moments beyond the obvious route.</p></div><b>↗</b></a><a href="/budget" className="capability-card"><span>04</span><div><strong>Smart Budget</strong><p>See the big picture and spend with confidence along the way.</p></div><b>↗</b></a></div></section>
      <section className="home-how" id="how-it-works"><div className="home-how-intro"><p className="home-eyebrow">How YatraAI works</p><h2>From first idea<br /><em>to ready to go.</em></h2><p>A little context is all it takes. YatraAI keeps learning with you, even when the plan needs to move.</p></div><div className="home-steps"><div><span>01</span><strong>Plan</strong><p>Share your destination, style and curiosities.</p></div><i>→</i><div><span>02</span><strong>AI Generates</strong><p>Receive a considered itinerary in moments.</p></div><i>→</i><div><span>03</span><strong>Situation Changes</strong><p>Weather, crowds or timing shift the day.</p></div><i>→</i><div><span>04</span><strong>AI Replans</strong><p>Keep moving with a better alternative.</p></div></div></section>
      <section className="home-final"><p className="home-eyebrow">Your next chapter starts here</p><h2>Make room for<br /><em>the unexpected.</em></h2><a className="home-cta home-cta-light" href="/planner">Plan My Trip <span aria-hidden="true">↗</span></a></section>
      <footer className="home-footer"><a className="brand" href="#top"><span className="brand-mark">Y</span><span>Yatra<span className="brand-accent">AI</span></span></a><span>Travel thoughtfully. Go far.</span><span>© 2026 YatraAI</span></footer>
    </main>
  )
}

export default App
