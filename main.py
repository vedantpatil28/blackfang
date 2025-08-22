#!/usr/bin/env python3
"""
BLACK FANG INTELLIGENCE - Production Application
Copy this ENTIRE code into main.py and deploy
"""
import os
import asyncio
import logging
from datetime import datetime
import hashlib
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import asyncpg
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/railway')

# Global database pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    logger.info("🚀 Starting Black Fang Intelligence...")
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        logger.info("✅ Database connected")
        await init_database()
        logger.info("✅ Database initialized")
        await create_demo_data()
        logger.info("✅ Demo data ready")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
    yield
    if db_pool:
        await db_pool.close()
    logger.info("🛑 Shutting down")

# Initialize FastAPI
app = FastAPI(
    title="Black Fang Intelligence",
    description="Real-time competitive intelligence platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_database():
    if not db_pool:
        return
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS competitors (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                name VARCHAR(255) NOT NULL,
                website VARCHAR(500),
                threat_level VARCHAR(20) DEFAULT 'MEDIUM',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                competitor_name VARCHAR(255) NOT NULL,
                alert_type VARCHAR(100) NOT NULL,
                severity VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS scraping_data (
                id SERIAL PRIMARY KEY,
                competitor_id INTEGER REFERENCES competitors(id),
                raw_data JSONB NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

async def create_demo_data():
    if not db_pool:
        return
    async with db_pool.acquire() as conn:
        existing = await conn.fetchrow("SELECT id FROM clients WHERE email='demo@blackfangintel.com'")
        if existing:
            return
        password_hash = hashlib.sha256('demo123'.encode()).hexdigest()
        client_id = await conn.fetchval("""
            INSERT INTO clients (name, email, password_hash, company)
            VALUES ($1, $2, $3, $4) RETURNING id
        """, 'Demo Automotive Dealership', 'demo@blackfangintel.com', password_hash, 'Demo Motors Pvt Ltd')
        competitors = [
            ('AutoMax Dealers', 'https://cars24.com', 'HIGH'),
            ('Speed Motors', 'https://carwale.com', 'MEDIUM'),
            ('Elite Auto', 'https://cardekho.com', 'LOW')
        ]
        for name, site, level in competitors:
            await conn.execute(
                "INSERT INTO competitors (client_id, name, website, threat_level) VALUES ($1,$2,$3,$4)",
                client_id, name, site, level
            )
        alerts = [
            ('AutoMax Dealers','PRICE_DROP','HIGH','Price dropped 8% on Honda City','Consider price matching'),
            ('Speed Motors','NEW_PROMOTION','MEDIUM','Monsoon Special 5% off','Counter-promotional')
        ]
        for comp, atype, sev, msg, rec in alerts:
            await conn.execute(
                "INSERT INTO alerts (client_id, competitor_name, alert_type, severity, message, recommendation) VALUES ($1,$2,$3,$4,$5,$6)",
                client_id, comp, atype, sev, msg, rec
            )

@app.get("/")
async def root():
    return {"message":"🎯 Black Fang Intelligence API","status":"operational","version":"1.0.0"}

@app.get("/health")
async def health():
    return {"status":"healthy","timestamp":datetime.utcnow().isoformat()}

@app.post("/api/auth/login")
async def login(request: Request):
    data = await request.json()
    if data.get('email')=='demo@blackfangintel.com' and data.get('password')=='demo123':
        return {"success":True,"client":{"id":1,"name":"Demo Automotive Dealership","email":"demo@blackfangintel.com"}}
    raise HTTPException(status_code=401,detail="Invalid credentials")

@app.get("/app", response_class=HTMLResponse)
async def serve_login_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Black Fang Intelligence</title></head>
    <body style="background:#0f0f0f;color:white;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;">
    <div style="background:#1a1a1a;padding:40px;border-radius:10px;text-align:center;">
    <h1 style="color:#dc2626;">⚡ BLACK FANG INTELLIGENCE</h1>
    <p style="margin-bottom:20px;">Demo login:</p>
    <form id="f">
      <input id="e" value="demo@blackfangintel.com" style="padding:10px;width:100%;margin-bottom:10px;background:#222;border:none;color:white;"><br>
      <input id="p" type="password" value="demo123" style="padding:10px;width:100%;background:#222;border:none;color:white;"><br>
      <button type="button" onclick="l()" style="padding:10px 20px;background:#dc2626;border:none;color:white;cursor:pointer;border-radius:5px;">Login</button>
    </form>
    <script>
      async function l(){
        let res=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('e').value,password:document.getElementById('p').value})});
        let j=await res.json();if(j.success)window.location.href='/dashboard';else alert('Login failed');
      }
    </script>
    </div>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    return "<h1>Dashboard Ready</h1><p>Implement UI here</p>"

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=int(os.getenv('PORT',8080)))