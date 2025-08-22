// BLACK FANG INTELLIGENCE - Application Logic

// Application data from provided JSON
const appData = {
  "competitors": [
    {
      "id": 1,
      "name": "AutoMax Dealers",
      "industry": "Automotive",
      "website": "https://automax-dealers.com",
      "threat_level": "HIGH",
      "last_activity": "2025-08-17T10:30:00Z",
      "changes_detected": 5,
      "price_changes": [
        {"model": "Honda City", "old_price": "₹12,50,000", "new_price": "₹11,75,000", "change": "-6%"},
        {"model": "Maruti Swift", "old_price": "₹7,80,000", "new_price": "₹7,50,000", "change": "-3.8%"}
      ],
      "recent_reviews": 3,
      "negative_reviews": 2,
      "promotions": ["Diwali Special - 10% off", "Free Insurance"]
    },
    {
      "id": 2,
      "name": "SmileCare Dental",
      "industry": "Healthcare",
      "website": "https://smilecare-dental.com",
      "threat_level": "MEDIUM",
      "last_activity": "2025-08-16T15:45:00Z",
      "changes_detected": 2,
      "price_changes": [
        {"service": "Teeth Cleaning", "old_price": "₹3,000", "new_price": "₹2,500", "change": "-16.7%"}
      ],
      "recent_reviews": 8,
      "negative_reviews": 1,
      "promotions": ["New Patient Special"]
    },
    {
      "id": 3,
      "name": "FitZone Gym",
      "industry": "Fitness",
      "website": "https://fitzone-gym.com", 
      "threat_level": "LOW",
      "last_activity": "2025-08-15T09:20:00Z",
      "changes_detected": 1,
      "price_changes": [],
      "recent_reviews": 5,
      "negative_reviews": 0,
      "promotions": ["Summer Membership - 3 months free"]
    }
  ],
  "alerts": [
    {
      "id": 1,
      "type": "PRICE_DROP",
      "competitor": "AutoMax Dealers",
      "severity": "HIGH",
      "message": "Price dropped 6% on Honda City - ₹75,000 reduction",
      "timestamp": "2025-08-17T10:30:00Z",
      "read": false,
      "recommendation": "Consider price matching or highlighting superior service value"
    },
    {
      "id": 2,
      "type": "NEGATIVE_REVIEWS",
      "competitor": "AutoMax Dealers", 
      "severity": "MEDIUM",
      "message": "2 negative reviews about delivery delays in past 24h",
      "timestamp": "2025-08-17T08:15:00Z",
      "read": false,
      "recommendation": "Target 'fast delivery' in your marketing campaigns"
    },
    {
      "id": 3,
      "type": "NEW_PROMOTION",
      "competitor": "SmileCare Dental",
      "severity": "MEDIUM", 
      "message": "Launched 'New Patient Special' discount program",
      "timestamp": "2025-08-16T15:45:00Z",
      "read": true,
      "recommendation": "Launch counter-promotional campaign for new patients"
    }
  ],
  "reports": [
    {
      "id": 1,
      "title": "Weekly Intelligence Report - Aug 12-17, 2025",
      "date": "2025-08-17",
      "competitors_monitored": 3,
      "total_changes": 8,
      "high_threats": 1,
      "key_insights": [
        "AutoMax Dealers aggressive pricing strategy - 3 price drops this week",
        "SmileCare expanding patient acquisition with discount programs", 
        "FitZone maintaining premium positioning with minimal changes"
      ],
      "recommendations": [
        "Immediate price review for Honda City model",
        "Launch 'Superior Service' campaign to differentiate from AutoMax",
        "Monitor SmileCare's discount effectiveness for potential response"
      ]
    },
    {
      "id": 2,
      "title": "Weekly Intelligence Report - Aug 5-11, 2025", 
      "date": "2025-08-11",
      "competitors_monitored": 3,
      "total_changes": 4,
      "high_threats": 0,
      "key_insights": [
        "Market stability across all competitors",
        "Standard promotional activities for seasonal sales",
        "No significant pricing or service changes detected"
      ]
    }
  ],
  "user_profile": {
    "name": "Vedant Patel",
    "company": "Demo Automotive Dealership", 
    "email": "vedant@example.com",
    "subscription": "Premium Plan",
    "monthly_fee": "₹65,000",
    "competitors_tracked": 3,
    "alerts_enabled": true,
    "report_frequency": "Weekly"
  },
  "pricing_plans": [
    {
      "name": "Basic Intelligence",
      "price": "₹25,000",
      "features": ["Up to 3 competitors", "Weekly reports", "Basic alerts", "Email support"],
      "popular": false
    },
    {
      "name": "Professional",
      "price": "₹45,000", 
      "features": ["Up to 7 competitors", "Real-time alerts", "Advanced analytics", "Phone support", "Custom reports"],
      "popular": true
    },
    {
      "name": "Enterprise",
      "price": "₹75,000",
      "features": ["Unlimited competitors", "Priority alerts", "Strategic consultation", "Dedicated support", "API access"],
      "popular": false
    }
  ]
};

// Application state
let currentSection = 'landing';
let isLoggedIn = false;

// DOM elements
const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.nav-link');
const sidebarLinks = document.querySelectorAll('.sidebar-link');
const sidebar = document.getElementById('sidebar');
const mainContent = document.querySelector('.main-content');

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    populateData();
});

function initializeApp() {
    showSection('landing');
    populatePricingPlans();
}

function setupEventListeners() {
    // Navigation event listeners - both nav and sidebar
    document.addEventListener('click', function(e) {
        // Handle navigation clicks
        if (e.target.classList.contains('nav-link') || e.target.classList.contains('sidebar-link')) {
            e.preventDefault();
            const section = e.target.getAttribute('data-section');
            if (section) {
                handleNavigation(section);
            }
        }
        
        // Handle Access Dashboard button
        if (e.target.id === 'accessDashboard') {
            e.preventDefault();
            isLoggedIn = true;
            handleNavigation('dashboard');
        }
        
        // Handle Add Competitor button
        if (e.target.id === 'addCompetitorBtn') {
            e.preventDefault();
            showAddCompetitorModal();
        }
        
        // Handle modal close buttons
        if (e.target.id === 'closeModal' || e.target.id === 'cancelModal') {
            e.preventDefault();
            hideAddCompetitorModal();
        }
        
        // Handle filter buttons
        if (e.target.classList.contains('filter-btn')) {
            e.preventDefault();
            handleAlertFilter(e);
        }
        
        // Handle modal background click
        if (e.target.id === 'addCompetitorModal') {
            hideAddCompetitorModal();
        }
        
        // Handle smooth scrolling for anchor links
        if (e.target.matches('a[href^="#"]')) {
            e.preventDefault();
            const target = document.querySelector(e.target.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });

    // Form submissions
    document.addEventListener('submit', function(e) {
        if (e.target.id === 'addCompetitorForm') {
            e.preventDefault();
            handleAddCompetitor(e);
        }
        
        if (e.target.id === 'contactForm') {
            e.preventDefault();
            handleContactForm(e);
        }
    });
}

function handleNavigation(section) {
    console.log('Navigating to:', section); // Debug log
    
    // Handle dashboard access and login state
    if (['dashboard', 'competitors', 'reports', 'alerts', 'settings'].includes(section)) {
        if (!isLoggedIn) {
            isLoggedIn = true;
        }
        showSidebar();
    }
    
    if (section === 'landing') {
        isLoggedIn = false;
        hideSidebar();
    }
    
    showSection(section);
    updateActiveLinks(section);
}

function showSection(sectionId) {
    console.log('Showing section:', sectionId); // Debug log
    
    // Hide all sections
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionId;
        
        // Re-populate data when section becomes active
        if (sectionId === 'dashboard') {
            populateDashboardAlerts();
            populateCompetitorOverview();
            populateActivityTimeline();
            createThreatChart();
        } else if (sectionId === 'competitors') {
            populateCompetitorsGrid();
        } else if (sectionId === 'reports') {
            populateReportsList();
        } else if (sectionId === 'alerts') {
            populateAlertsList();
        } else if (sectionId === 'settings') {
            populateProfileInfo();
            populateSubscriptionInfo();
        }
    }
}

function showSidebar() {
    if (sidebar) {
        sidebar.classList.remove('hidden');
    }
    if (mainContent) {
        mainContent.classList.add('with-sidebar');
    }
}

function hideSidebar() {
    if (sidebar) {
        sidebar.classList.add('hidden');
    }
    if (mainContent) {
        mainContent.classList.remove('with-sidebar');
    }
}

function updateActiveLinks(section) {
    // Update sidebar links
    sidebarLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === section) {
            link.classList.add('active');
        }
    });
    
    // Update nav links
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === section) {
            link.classList.add('active');
        }
    });
}

function showAddCompetitorModal() {
    const modal = document.getElementById('addCompetitorModal');
    if (modal) {
        modal.classList.remove('hidden');
        console.log('Modal shown'); // Debug log
    }
}

function hideAddCompetitorModal() {
    const modal = document.getElementById('addCompetitorModal');
    if (modal) {
        modal.classList.add('hidden');
        console.log('Modal hidden'); // Debug log
    }
}

function populateData() {
    populateDashboardAlerts();
    populateCompetitorOverview();
    populateActivityTimeline();
    populateCompetitorsGrid();
    populateReportsList();
    populateAlertsList();
    populateProfileInfo();
    populateSubscriptionInfo();
    // Chart will be created when dashboard section is shown
}

function populatePricingPlans() {
    const pricingGrid = document.getElementById('pricingGrid');
    if (!pricingGrid) return;

    pricingGrid.innerHTML = appData.pricing_plans.map(plan => `
        <div class="pricing-card ${plan.popular ? 'popular' : ''}">
            <div class="pricing-name">${plan.name}</div>
            <div class="pricing-price">${plan.price}</div>
            <div class="pricing-period">per month</div>
            <ul class="pricing-features">
                ${plan.features.map(feature => `<li>${feature}</li>`).join('')}
            </ul>
            <button class="btn btn--primary btn--full-width">Choose Plan</button>
        </div>
    `).join('');
}

function populateDashboardAlerts() {
    const alertsContainer = document.getElementById('dashboardAlerts');
    if (!alertsContainer) return;

    const unreadAlerts = appData.alerts.filter(alert => !alert.read).slice(0, 3);
    
    alertsContainer.innerHTML = unreadAlerts.map(alert => `
        <div class="alert-item">
            <div class="alert-severity ${alert.severity}"></div>
            <div class="alert-content">
                <div class="alert-message">${alert.message}</div>
                <div class="alert-time">${formatTime(alert.timestamp)}</div>
                ${alert.recommendation ? `<div class="alert-recommendation">${alert.recommendation}</div>` : ''}
            </div>
        </div>
    `).join('');
}

function populateCompetitorOverview() {
    const container = document.getElementById('competitorOverview');
    if (!container) return;

    container.innerHTML = appData.competitors.map(competitor => `
        <div class="competitor-item">
            <div class="competitor-info">
                <div class="competitor-name">${competitor.name}</div>
                <div class="competitor-industry">${competitor.industry}</div>
            </div>
            <div class="threat-level ${competitor.threat_level}">${competitor.threat_level}</div>
        </div>
    `).join('');
}

function populateActivityTimeline() {
    const container = document.getElementById('activityTimeline');
    if (!container) return;

    const activities = [
        { message: "AutoMax Dealers reduced Honda City price by 6%", time: "2025-08-17T10:30:00Z" },
        { message: "SmileCare Dental launched new patient promotion", time: "2025-08-16T15:45:00Z" },
        { message: "AutoMax Dealers received negative reviews", time: "2025-08-17T08:15:00Z" },
        { message: "FitZone Gym updated membership packages", time: "2025-08-15T09:20:00Z" }
    ];

    container.innerHTML = activities.map(activity => `
        <div class="alert-item">
            <div class="alert-content">
                <div class="alert-message">${activity.message}</div>
                <div class="alert-time">${formatTime(activity.time)}</div>
            </div>
        </div>
    `).join('');
}

function populateCompetitorsGrid() {
    const container = document.getElementById('competitorsGrid');
    if (!container) return;

    container.innerHTML = appData.competitors.map(competitor => `
        <div class="competitor-card">
            <div class="competitor-header">
                <div class="competitor-details">
                    <h3>${competitor.name}</h3>
                    <div class="competitor-industry">${competitor.industry}</div>
                    <a href="${competitor.website}" target="_blank" class="competitor-website">${competitor.website}</a>
                </div>
                <div class="threat-level ${competitor.threat_level}">${competitor.threat_level}</div>
            </div>
            
            <div class="competitor-stats">
                <p><strong>Changes Detected:</strong> ${competitor.changes_detected}</p>
                <p><strong>Recent Reviews:</strong> ${competitor.recent_reviews} (${competitor.negative_reviews} negative)</p>
                <p><strong>Last Activity:</strong> ${formatTime(competitor.last_activity)}</p>
            </div>

            ${competitor.price_changes.length > 0 ? `
                <div class="price-changes">
                    <h4>Recent Price Changes</h4>
                    ${competitor.price_changes.map(change => `
                        <div class="price-change">
                            <span>${change.model || change.service}</span>
                            <span class="price-change-negative">${change.change}</span>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            ${competitor.promotions.length > 0 ? `
                <div class="promotions">
                    <h4>Active Promotions</h4>
                    ${competitor.promotions.map(promo => `
                        <span class="promotion-tag">${promo}</span>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

function populateReportsList() {
    const container = document.getElementById('reportsList');
    if (!container) return;

    container.innerHTML = appData.reports.map(report => `
        <div class="report-card">
            <div class="report-header">
                <div>
                    <div class="report-title">${report.title}</div>
                    <div class="report-date">${formatDate(report.date)}</div>
                </div>
                <button class="btn btn--outline">View Report</button>
            </div>
            
            <div class="report-stats">
                <div class="report-stat">
                    <div class="report-stat-number">${report.competitors_monitored}</div>
                    <div class="report-stat-label">Competitors</div>
                </div>
                <div class="report-stat">
                    <div class="report-stat-number">${report.total_changes}</div>
                    <div class="report-stat-label">Changes</div>
                </div>
                <div class="report-stat">
                    <div class="report-stat-number">${report.high_threats}</div>
                    <div class="report-stat-label">High Threats</div>
                </div>
            </div>

            ${report.key_insights ? `
                <div class="report-insights">
                    <h4>Key Insights</h4>
                    <ul>
                        ${report.key_insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}

            ${report.recommendations ? `
                <div class="report-recommendations">
                    <h4>Recommendations</h4>
                    <ul>
                        ${report.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `).join('');
}

function populateAlertsList() {
    const container = document.getElementById('alertsList');
    if (!container) return;

    container.innerHTML = appData.alerts.map(alert => `
        <div class="alert-card ${alert.severity}" data-severity="${alert.severity}">
            <div class="alert-card-header">
                <div>
                    <div class="alert-type">${alert.type.replace('_', ' ')}</div>
                    <div class="alert-competitor">${alert.competitor}</div>
                </div>
                <div class="threat-level ${alert.severity}">${alert.severity}</div>
            </div>
            <div class="alert-message">${alert.message}</div>
            <div class="alert-time">${formatTime(alert.timestamp)}</div>
            ${alert.recommendation ? `<div class="alert-recommendation">${alert.recommendation}</div>` : ''}
        </div>
    `).join('');
}

function populateProfileInfo() {
    const container = document.getElementById('profileInfo');
    if (!container) return;

    const profile = appData.user_profile;
    container.innerHTML = `
        <div class="profile-field">
            <span class="profile-label">Name</span>
            <span class="profile-value">${profile.name}</span>
        </div>
        <div class="profile-field">
            <span class="profile-label">Company</span>
            <span class="profile-value">${profile.company}</span>
        </div>
        <div class="profile-field">
            <span class="profile-label">Email</span>
            <span class="profile-value">${profile.email}</span>
        </div>
        <div class="profile-field">
            <span class="profile-label">Competitors Tracked</span>
            <span class="profile-value">${profile.competitors_tracked}</span>
        </div>
    `;
}

function populateSubscriptionInfo() {
    const container = document.getElementById('subscriptionInfo');
    if (!container) return;

    const profile = appData.user_profile;
    container.innerHTML = `
        <div class="subscription-plan">
            <div class="subscription-plan-name">${profile.subscription}</div>
            <div class="subscription-plan-price">${profile.monthly_fee}/month</div>
        </div>
        <div class="profile-field">
            <span class="profile-label">Report Frequency</span>
            <span class="profile-value">${profile.report_frequency}</span>
        </div>
        <div class="profile-field">
            <span class="profile-label">Alerts Enabled</span>
            <span class="profile-value">${profile.alerts_enabled ? 'Yes' : 'No'}</span>
        </div>
        <button class="btn btn--primary btn--full-width">Upgrade Plan</button>
    `;
}

function createThreatChart() {
    const canvas = document.getElementById('threatChart');
    if (!canvas || canvas.chart) return; // Prevent duplicate charts

    const ctx = canvas.getContext('2d');
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Aug 13', 'Aug 14', 'Aug 15', 'Aug 16', 'Aug 17'],
            datasets: [{
                label: 'High Threats',
                data: [0, 0, 0, 1, 1],
                borderColor: '#dc2626',
                backgroundColor: 'rgba(220, 38, 38, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Medium Threats',
                data: [1, 1, 2, 2, 2],
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Low Threats',
                data: [1, 1, 1, 1, 1],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#b0b0b0'
                    },
                    grid: {
                        color: '#404040'
                    }
                },
                y: {
                    ticks: {
                        color: '#b0b0b0'
                    },
                    grid: {
                        color: '#404040'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function handleAddCompetitor(e) {
    e.preventDefault();
    
    // In a real app, this would send data to the server
    alert('Competitor added successfully! (This is a demo)');
    
    // Close modal
    hideAddCompetitorModal();
    
    // Reset form
    e.target.reset();
}

function handleContactForm(e) {
    e.preventDefault();
    
    // In a real app, this would send data to the server
    alert('Thank you for your message! Our team will contact you soon.');
    
    // Reset form
    e.target.reset();
}

function handleAlertFilter(e) {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const alertCards = document.querySelectorAll('.alert-card');
    const filterValue = e.target.dataset.filter;
    
    console.log('Filtering by:', filterValue); // Debug log
    
    // Update active filter button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    e.target.classList.add('active');
    
    // Filter alert cards
    alertCards.forEach(card => {
        if (filterValue === 'all' || card.dataset.severity === filterValue) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Utility functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
        return 'Just now';
    } else if (diffInHours < 24) {
        return `${diffInHours}h ago`;
    } else {
        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays}d ago`;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}