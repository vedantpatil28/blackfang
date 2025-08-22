#!/usr/bin/env python3
"""
BLACK FANG INTELLIGENCE - Production Application
Copy this ENTIRE code into a file named main.py
"""
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Black Fang Intelligence", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🎯 Black Fang Intelligence API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-08-22"}

@app.post("/api/auth/login")
async def login(request: Request):
    try:
        body = await request.json()
        email = body.get('email', '')
        password = body.get('password', '')
        
        # Simple demo authentication
        if email == 'demo@blackfangintel.com' and password == 'demo123':
            return {
                "success": True,
                "client": {
                    "id": 1,
                    "name": "Demo Automotive Dealership",
                    "email": email,
                    "company": "Demo Motors Pvt Ltd"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Login failed")

@app.get("/app", response_class=HTMLResponse)
async def serve_login_page():
    """Serve the main login page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Black Fang Intelligence</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 50px;
            }
            .brand {
                color: #dc2626;
                font-size: 48px;
                font-weight: bold;
                text-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
                margin-bottom: 10px;
            }
            .tagline {
                color: #888;
                font-size: 24px;
                font-weight: 300;
            }
            .login-section {
                max-width: 500px;
                margin: 0 auto;
            }
            .login-form {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                border: 1px solid #333;
            }
            .form-title {
                color: #dc2626;
                font-size: 28px;
                margin-bottom: 30px;
                text-align: center;
            }
            .form-group {
                margin-bottom: 25px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #ccc;
                font-weight: 500;
            }
            .form-group input {
                width: 100%;
                padding: 15px;
                border: 2px solid #333;
                background: #0f0f0f;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            .form-group input:focus {
                border-color: #dc2626;
                outline: none;
                background: #1a1a1a;
                box-shadow: 0 0 10px rgba(220, 38, 38, 0.3);
            }
            .btn {
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                width: 100%;
                font-size: 18px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(220, 38, 38, 0.4);
            }
            .btn:active {
                transform: translateY(0);
            }
            .demo-info {
                background: #0f0f0f;
                padding: 25px;
                border-radius: 15px;
                margin-top: 25px;
                border-left: 5px solid #dc2626;
            }
            .demo-info h3 {
                color: #dc2626;
                margin-bottom: 15px;
                font-size: 20px;
            }
            .demo-info p {
                margin-bottom: 10px;
                line-height: 1.5;
            }
            .loading {
                display: none;
                text-align: center;
                margin-top: 20px;
            }
            .spinner {
                border: 3px solid #333;
                border-top: 3px solid #dc2626;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
                margin-top: 50px;
            }
            .feature {
                background: #1a1a1a;
                padding: 30px;
                border-radius: 15px;
                border-left: 5px solid #dc2626;
                transition: transform 0.3s ease;
            }
            .feature:hover {
                transform: translateY(-5px);
            }
            .feature h4 {
                color: #dc2626;
                margin-bottom: 15px;
                font-size: 18px;
            }
            .feature p {
                line-height: 1.6;
                color: #ccc;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="brand">⚡ BLACK FANG INTELLIGENCE</div>
                <div class="tagline">We see what they hide. You win.</div>
            </div>
            
            <div class="login-section">
                <div class="login-form">
                    <h2 class="form-title">Intelligence Dashboard Access</h2>
                    
                    <form id="loginForm">
                        <div class="form-group">
                            <label>Email Address:</label>
                            <input type="email" id="email" value="demo@blackfangintel.com" required>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input type="password" id="password" value="demo123" required>
                        </div>
                        <button type="submit" class="btn">Access Intelligence Dashboard</button>
                    </form>
                    
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>Authenticating and loading dashboard...</p>
                    </div>
                    
                    <div class="demo-info">
                        <h3>🎯 Demo Account Access</h3>
                        <p><strong>Email:</strong> demo@blackfangintel.com</p>
                        <p><strong>Password:</strong> demo123</p>
                        <p>Experience a complete competitive intelligence dashboard for an automotive dealership with live competitor monitoring and strategic insights.</p>
                    </div>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h4>🔍 Real-time Monitoring</h4>
                        <p>24/7 automated tracking of competitor websites, pricing, and promotional activities with instant detection of changes.</p>
                    </div>
                    <div class="feature">
                        <h4>🚨 Instant Alerts</h4>
                        <p>Immediate notifications for critical competitor moves like price drops, new promotions, and market changes.</p>
                    </div>
                    <div class="feature">
                        <h4>📊 Strategic Insights</h4>
                        <p>AI-powered analysis with actionable recommendations for competitive response and market positioning.</p>
                    </div>
                    <div class="feature">
                        <h4>📱 Professional Dashboard</h4>
                        <p>Comprehensive intelligence overview with threat levels, competitive analysis, and strategic recommendations.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const loading = document.getElementById('loading');
                const form = document.getElementById('loginForm');
                
                // Show loading
                form.style.display = 'none';
                loading.style.display = 'block';
                
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Redirect to dashboard
                        window.location.href = `/dashboard?client_id=${data.client.id}`;
                    } else {
                        alert('Login failed: Invalid credentials');
                        form.style.display = 'block';
                        loading.style.display = 'none';
                    }
                } catch (error) {
                    alert('Connection error. Please check your credentials.');
                    form.style.display = 'block';
                    loading.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(client_id: int = 1):
    """Serve the client dashboard"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Black Fang Intelligence - Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
                color: white;
                margin: 0;
                min-height: 100vh;
            }
            .header {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 20px 0;
                border-bottom: 3px solid #dc2626;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .brand {
                color: #dc2626;
                font-size: 28px;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
            }
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 10px;
                color: #888;
            }
            .live-dot {
                width: 8px;
                height: 8px;
                background: #10b981;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px 20px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }
            .stat-card {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 30px;
                border-radius: 15px;
                border-left: 6px solid #dc2626;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }
            .stat-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 35px rgba(220, 38, 38, 0.2);
            }
            .stat-number {
                font-size: 42px;
                font-weight: bold;
                color: #dc2626;
                margin-bottom: 8px;
                text-shadow: 0 0 10px rgba(220, 38, 38, 0.3);
            }
            .stat-label {
                color: #888;
                font-size: 16px;
                font-weight: 500;
            }
            .section {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 35px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                border: 1px solid #333;
            }
            .section h2 {
                color: #dc2626;
                margin-bottom: 25px;
                font-size: 26px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .alert {
                background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
                padding: 25px;
                margin: 20px 0;
                border-radius: 12px;
                border-left: 6px solid;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .alert:hover {
                transform: translateX(10px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            }
            .alert.high {
                border-left-color: #dc2626;
                background: linear-gradient(135deg, #2d1a1a 0%, #3a2222 100%);
            }
            .alert.medium {
                border-left-color: #f59e0b;
                background: linear-gradient(135deg, #2d2a1a 0%, #3a3222 100%);
            }
            .alert.low {
                border-left-color: #10b981;
                background: linear-gradient(135deg, #1a2d26 0%, #223a32 100%);
            }
            .alert h4 {
                margin-bottom: 12px;
                font-size: 18px;
                color: #fff;
            }
            .alert p {
                margin-bottom: 10px;
                line-height: 1.6;
                color: #ddd;
            }
            .alert small {
                color: #888;
                font-size: 13px;
            }
            .competitor {
                background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
                padding: 25px;
                margin: 20px 0;
                border-radius: 12px;
                border-left: 6px solid #666;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .competitor:hover {
                transform: translateX(10px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
                border-left-color: #dc2626;
            }
            .competitor h4 {
                margin-bottom: 12px;
                color: #fff;
                font-size: 18px;
            }
            .competitor p {
                margin-bottom: 8px;
                line-height: 1.5;
                color: #ddd;
            }
            .status-high {
                color: #dc2626;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(220, 38, 38, 0.5);
            }
            .status-medium {
                color: #f59e0b;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(245, 158, 11, 0.5);
            }
            .status-low {
                color: #10b981;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(16, 185, 129, 0.5);
            }
            .refresh-btn {
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                margin-bottom: 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .refresh-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(220, 38, 38, 0.4);
            }
            .last-updated {
                color: #666;
                font-size: 12px;
                text-align: right;
                margin-top: 20px;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="brand">⚡ BLACK FANG INTELLIGENCE</div>
                <div class="status-indicator">
                    <div class="live-dot"></div>
                    <span>Live Monitoring Active</span>
                    <span id="currentTime"></span>
                </div>
            </div>
        </div>
        
        <div class="container">
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Intelligence Data</button>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div class="stat-label">Competitors Monitored</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Active Threat Alerts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">2</div>
                    <div class="stat-label">High Priority Threats</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Real-time Monitoring</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🚨 Critical Threat Intelligence</h2>
                
                <div class="alert high">
                    <h4>🔴 HIGH PRIORITY: Price War Detected - AutoMax Dealers</h4>
                    <p><strong>Intelligence:</strong> Competitor dropped Honda City prices by 8% (₹95,000 reduction). Immediate market share impact detected.</p>
                    <p><strong>Strategic Response:</strong> Consider immediate price matching or launch "Superior Service Value" campaign highlighting your competitive advantages.</p>
                    <small>⏰ Detected: 2 hours ago | Confidence Level: 95% | Source: Price Monitoring System</small>
                </div>
                
                <div class="alert medium">
                    <h4>🟡 MEDIUM ALERT: Aggressive Promotion Launch - Speed Motors</h4>
                    <p><strong>Intelligence:</strong> New promotional campaign "Monsoon Special - Extra 5% off + Free Insurance" launched across all digital channels.</p>
                    <p><strong>Strategic Response:</strong> Deploy counter-promotional strategy within 48 hours to prevent customer migration and maintain market position.</p>
                    <small>⏰ Detected: 5 hours ago | Confidence Level: 88% | Source: Social Media & Website Monitoring</small>
                </div>
                
                <div class="alert medium">
                    <h4>🟡 REPUTATION OPPORTUNITY: Service Issues - Elite Auto</h4>
                    <p><strong>Intelligence:</strong> 3 negative reviews posted in past 24 hours citing delivery delays and poor customer service response times.</p>
                    <p><strong>Strategic Response:</strong> Target "Fast & Reliable Service" messaging in marketing campaigns to capitalize on competitor weakness.</p>
                    <small>⏰ Detected: 8 hours ago | Confidence Level: 92% | Source: Review Monitoring System</small>
                </div>
            </div>
            
            <div class="section">
                <h2>👥 Competitor Intelligence Network</h2>
                
                <div class="competitor">
                    <h4>🎯 AutoMax Dealers</h4>
                    <p><strong>Website:</strong> cars24.com | <strong>Industry:</strong> Automotive Dealership</p>
                    <p><strong>Threat Level:</strong> <span class="status-high">HIGH ACTIVITY</span> | <strong>Last Update:</strong> 2 hours ago</p>
                    <p><strong>Key Intelligence:</strong> Aggressive pricing strategy detected. 8% price reduction on premium models. Targeting market share expansion through competitive pricing.</p>
                    <p><strong>Market Position:</strong> Primary threat - direct competitor with similar customer base and service offerings.</p>
                </div>
                
                <div class="competitor">
                    <h4>⚡ Speed Motors</h4>
                    <p><strong>Website:</strong> carwale.com | <strong>Industry:</strong> Automotive Dealership</p>
                    <p><strong>Threat Level:</strong> <span class="status-medium">MEDIUM ACTIVITY</span> | <strong>Last Update:</strong> 5 hours ago</p>
                    <p><strong>Key Intelligence:</strong> Promotional focus with seasonal campaigns. Moderate pricing adjustments. Strong digital marketing presence.</p>
                    <p><strong>Market Position:</strong> Secondary threat - competitive in promotional strategies and customer acquisition.</p>
                </div>
                
                <div class="competitor">
                    <h4>🚗 Elite Auto</h4>
                    <p><strong>Website:</strong> cardekho.com | <strong>Industry:</strong> Automotive Dealership</p>
                    <p><strong>Threat Level:</strong> <span class="status-low">LOW ACTIVITY</span> | <strong>Last Update:</strong> 1 day ago</p>
                    <p><strong>Key Intelligence:</strong> Service quality issues emerging. Customer complaints about delivery delays. Potential market opportunity for superior service positioning.</p>
                    <p><strong>Market Position:</strong> Minimal threat - declining service quality presents competitive advantage opportunity.</p>
                </div>
                
                <div class="last-updated">
                    Intelligence last updated: <span id="lastUpdated">Just now</span> | Next update: <span id="nextUpdate">In 6 hours</span>
                </div>
            </div>
        </div>
        
        <script>
            function updateTime() {
                const now = new Date();
                document.getElementById('currentTime').textContent = now.toLocaleTimeString();
            }
            
            function refreshData() {
                document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
                // Simulate data refresh
                alert('Intelligence data refreshed successfully!');
            }
            
            // Update time every second
            setInterval(updateTime, 1000);
            updateTime();
            
            // Auto-refresh indication every 30 seconds
            setInterval(() => {
                document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
            }, 30000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)