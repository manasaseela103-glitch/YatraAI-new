import {
  adminStats,
  aiInsights,
  analyticsData,
  businessExperiences,
  businessProfile,
  businessStats,
  destinationAnalytics,
  hiddenGemImpact,
  localEconomy,
  offers,
  touristLeads,
  tourismOverview,
} from './dashboardData.js'

export function BusinessDashboard() {
  return (
    <div className="dashboard-shell business-shell">
      <aside className="dashboard-sidebar">
        <a className="brand dashboard-brand" href="#/">
          <span className="brand-mark">Y</span>
          <span>Yatra<span className="brand-accent">AI</span></span>
        </a>

        <nav className="dashboard-nav" aria-label="Business dashboard navigation">
          <a href="#/business" className="active">Overview</a>
          <a href="#/planner">Plan a trip</a>
          <a href="#/explore">Discover</a>
          <a href="#/admin">Admin view</a>
        </nav>
      </aside>

      <main className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow"><span></span> Business Hub</p>
            <h1>YatraAI Business Hub</h1>
            <p className="dashboard-subtitle">Connect your local business with travelers looking for authentic experiences.</p>
          </div>
          <button className="primary-button" type="button">View Live Profile <span aria-hidden="true">↗</span></button>
        </header>

        <section className="stats-grid" aria-label="Business metrics">
          {businessStats.map((stat) => (
            <article key={stat.label} className="stat-card">
              <span>{stat.label}</span>
              <strong>{stat.value}</strong>
              <small>{stat.change}</small>
            </article>
          ))}
        </section>

        <section className="dashboard-grid">
          <article className="panel panel-large">
            <div className="panel-header">
              <h2>Business Profile</h2>
              <button type="button" className="secondary-button small-button">Edit Profile</button>
            </div>

            <div className="profile-row">
              <div className="profile-badge">HC</div>
              <div className="profile-copy">
                <h3>{businessProfile.name}</h3>
                <p>{businessProfile.category} • {businessProfile.location}</p>
              </div>
              <div className="rating-pill">★ {businessProfile.rating}</div>
            </div>

            <div className="profile-fields">
              <div>
                <label>Business name</label>
                <p>{businessProfile.name}</p>
              </div>
              <div>
                <label>Category</label>
                <p>{businessProfile.category}</p>
              </div>
              <div>
                <label>Location</label>
                <p>{businessProfile.location}</p>
              </div>
              <div>
                <label>Rating</label>
                <p>{businessProfile.rating} / 5</p>
              </div>
            </div>

            <div className="description-box">
              <label>Description</label>
              <p>{businessProfile.description}</p>
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <h2>Tourist Leads</h2>
            </div>

            <div className="lead-list">
              {touristLeads.map((lead) => (
                <div key={`${lead.tourist}-${lead.date}`} className="lead-item">
                  <div>
                    <strong>{lead.tourist}</strong>
                    <span>{lead.destination}</span>
                  </div>
                  <div>
                    <small>{lead.experience}</small>
                    <p>{lead.date}</p>
                  </div>
                  <span className={`status-badge ${lead.status.toLowerCase().replace(/\s+/g, '-')}`}>{lead.status}</span>
                </div>
              ))}
            </div>
          </article>

          <article className="panel panel-wide">
            <div className="panel-header">
              <h2>My Experiences</h2>
            </div>

            <div className="experience-grid">
              {businessExperiences.map((item) => (
                <div key={item.name} className="experience-card">
                  <div className="experience-topline">
                    <span>{item.status}</span>
                    <strong>{item.rating} ★</strong>
                  </div>
                  <h3>{item.name}</h3>
                  <div className="experience-metrics">
                    <div><small>Price</small><b>{item.price}</b></div>
                    <div><small>Views</small><b>{item.views}</b></div>
                    <div><small>Bookings</small><b>{item.bookings}</b></div>
                  </div>
                </div>
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <h2>Offers</h2>
            </div>

            <div className="offer-list">
              {offers.map((offer) => (
                <div key={offer.name} className="offer-item">
                  <div>
                    <strong>{offer.name}</strong>
                    <p>{offer.discount}</p>
                  </div>
                  <div className="offer-meta">
                    <small>{offer.validity}</small>
                    <span className={offer.active ? 'active' : 'inactive'}>{offer.active ? 'Active' : 'Inactive'}</span>
                  </div>
                </div>
              ))}
            </div>
          </article>

          <article className="panel panel-wide">
            <div className="panel-header">
              <h2>Analytics</h2>
            </div>

            <div className="analytics-bars">
              {analyticsData.map((item) => (
                <div key={item.label} className="analytics-row">
                  <div className="analytics-label-row">
                    <span>{item.label}</span>
                    <strong>{item.value}%</strong>
                  </div>
                  <div className="bar-track">
                    <span style={{ width: `${item.value}%` }}></span>
                  </div>
                </div>
              ))}
            </div>
          </article>
        </section>
      </main>
    </div>
  )
}

export function AdminDashboard() {
  return (
    <div className="admin-shell">
      <header className="admin-header">
        <div>
          <p className="eyebrow"><span></span> Intelligence</p>
          <h1>Tourism Intelligence Dashboard</h1>
          <p className="dashboard-subtitle">AI-powered insights for smarter tourism management.</p>
        </div>
      </header>

      <section className="stats-grid admin-stats" aria-label="Tourism metrics">
        {adminStats.map((stat) => (
          <article key={stat.label} className="stat-card admin-card">
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
          </article>
        ))}
      </section>

      <section className="admin-grid">
        <article className="panel panel-wide">
          <div className="panel-header">
            <h2>Tourism Overview</h2>
          </div>
          <div className="overview-chart">
            {tourismOverview.map((item) => (
              <div key={item.label} className="overview-item">
                <div className="chart-labels">
                  <span>{item.label}</span>
                  <strong>{item.value}%</strong>
                </div>
                <div className="bar-track chart-track">
                  <span style={{ width: `${item.value}%` }}></span>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="panel panel-wide">
          <div className="panel-header">
            <h2>Destination Analytics</h2>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Destination</th>
                  <th>Visitors</th>
                  <th>Crowd</th>
                  <th>Avg Spend</th>
                  <th>Trend</th>
                </tr>
              </thead>
              <tbody>
                {destinationAnalytics.map((item) => (
                  <tr key={item.destination}>
                    <td>{item.destination}</td>
                    <td>{item.visitors}</td>
                    <td><span className={`crowd-pill ${item.crowd.toLowerCase()}`}>{item.crowd}</span></td>
                    <td>{item.spending}</td>
                    <td>{item.trend}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Hidden Gem Impact</h2>
          </div>
          <div className="mini-stats">
            {hiddenGemImpact.map((item) => (
              <div key={item.label} className="mini-stat">
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Local Economy</h2>
          </div>
          <div className="mini-stats">
            {localEconomy.map((item) => (
              <div key={item.label} className="mini-stat">
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel panel-wide">
          <div className="panel-header">
            <h2>AI Tourism Insights</h2>
          </div>

          <div className="insight-cards">
            {aiInsights.map((insight) => (
              <div key={insight.title} className="insight-card-admin">
                <span>{insight.title}</span>
                <p>{insight.text}</p>
              </div>
            ))}
          </div>
        </article>
      </section>
    </div>
  )
}

export function BudgetPage() {
  return (
    <div className="simple-route-page">
      <div className="simple-route-card">
        <p className="eyebrow"><span></span> Budget Planning</p>
        <h1>Travel budget dashboard</h1>
        <p>Keep an eye on destination spending, activity budgets, and trip value in a single view.</p>
      </div>
    </div>
  )
}

export function SafetyPage() {
  return (
    <div className="simple-route-page">
      <div className="simple-route-card">
        <p className="eyebrow"><span></span> Safety Guide</p>
        <h1>Travel safety overview</h1>
        <p>Review safety notes, alternate routes, emergency contact guidance, and travel readiness details.</p>
      </div>
    </div>
  )
}
