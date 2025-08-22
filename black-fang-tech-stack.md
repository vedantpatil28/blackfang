# BLACK FANG - Complete Technical Implementation

## Project Structure
```
blackfang/
│
├── scrapers/
│   ├── website_scraper.py
│   ├── review_scraper.py
│   ├── ad_scraper.py
│   ├── social_scraper.py
│
├── analysis/
│   ├── change_detector.py
│   ├── sentiment_analyzer.py
│
├── reports/
│   ├── report_generator.py
│   ├── templates/
│   └── war_report_template.html
│
├── delivery/
│   ├── email_sender.py
│   ├── alert_notifier.py
│
├── data/
│   ├── old_data.json
│   ├── new_data.json
│
├── main.py
├── config.json
└── requirements.txt
```

## Core Technology Stack

### Data Collection Layer
- **Python Libraries**: `requests`, `BeautifulSoup4`, `scrapy`, `selenium`
- **APIs**: Google Maps API (reviews), Facebook Ad Library API
- **Web Scraping**: Static HTML parsing and dynamic JavaScript content

### Data Processing Layer
- **Data Management**: `pandas` for data manipulation, SQLite for storage
- **Text Processing**: `regex` for pattern extraction, `textblob` for sentiment analysis
- **Change Detection**: Custom algorithms to identify competitor moves

### Report Generation Layer
- **PDF Creation**: `reportlab` or `pdfkit` for automated report generation
- **Visualization**: `matplotlib` for charts and trend graphs
- **Templates**: HTML/CSS templates for consistent branding

### Delivery & Automation Layer
- **Email Automation**: SMTP integration for report delivery
- **Scheduling**: GitHub Actions or cron jobs for automated scraping
- **Notifications**: Telegram Bot API for instant alerts

## Installation & Setup

### Requirements (requirements.txt)
```
requests==2.31.0
beautifulsoup4==4.12.2
scrapy==2.11.0
selenium==4.15.0
pandas==2.0.3
textblob==0.17.1
reportlab==4.0.4
matplotlib==3.7.2
fpdf2==2.7.4
```

### Configuration (config.json)
```json
{
  "client_name": "Black Fang Demo",
  "competitor_url": "https://competitorwebsite.com",
  "google_place_id": "YOUR_PLACE_ID",
  "google_api_key": "YOUR_GOOGLE_API_KEY",
  "facebook_page_id": "YOUR_FB_PAGE_ID",
  "email": {
    "sender": "your_email@gmail.com",
    "password": "your_password",
    "recipient": "client_email@gmail.com"
  }
}
```

## Core Implementation Files

### 1. Website Scraper (scrapers/website_scraper.py)
```python
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

def scrape_static(url):
    """Scrape static HTML content"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract prices using regex
    price_pattern = r'₹[\d,]+'
    prices = re.findall(price_pattern, response.text)
    
    # Extract promotional content
    promo_keywords = ['sale', 'discount', 'offer', 'deal', 'limited']
    promos = []
    for keyword in promo_keywords:
        if keyword.lower() in response.text.lower():
            promos.append(keyword)
    
    return {
        'url': url,
        'prices': prices,
        'promotions': promos,
        'text_content': soup.get_text(separator=' ', strip=True)[:1000]
    }

def scrape_dynamic(url):
    """Scrape JavaScript-heavy websites"""
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)
```

### 2. Review Scraper (scrapers/review_scraper.py)
```python
import requests
from textblob import TextBlob

def fetch_google_reviews(place_id, api_key):
    """Fetch Google Maps reviews"""
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}&fields=reviews,rating"
    
    response = requests.get(url)
    data = response.json()
    reviews = []
    
    if 'result' in data and 'reviews' in data['result']:
        for review in data['result']['reviews']:
            sentiment = TextBlob(review['text']).sentiment
            reviews.append({
                "author": review['author_name'],
                "rating": review['rating'],
                "text": review['text'],
                "sentiment": "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral",
                "time": review['time']
            })
    
    return reviews

def analyze_review_trends(reviews):
    """Analyze review trends and sentiment changes"""
    recent_reviews = sorted(reviews, key=lambda x: x['time'], reverse=True)[:10]
    
    negative_count = len([r for r in recent_reviews if r['sentiment'] == 'Negative'])
    
    return {
        'total_recent': len(recent_reviews),
        'negative_count': negative_count,
        'negative_percentage': (negative_count / len(recent_reviews)) * 100 if recent_reviews else 0,
        'recent_negative_reviews': [r for r in recent_reviews if r['sentiment'] == 'Negative']
    }
```

### 3. Change Detection (analysis/change_detector.py)
```python
import json
from datetime import datetime

def detect_price_changes(old_data, new_data):
    """Detect price changes between datasets"""
    changes = []
    
    old_prices = set(old_data.get('prices', []))
    new_prices = set(new_data.get('prices', []))
    
    # New prices not in old data
    price_increases = new_prices - old_prices
    price_decreases = old_prices - new_prices
    
    if price_increases:
        changes.append({
            'type': 'price_increase',
            'description': f"New prices detected: {list(price_increases)}",
            'severity': 'medium'
        })
    
    if price_decreases:
        changes.append({
            'type': 'price_decrease', 
            'description': f"Price drops detected: {list(price_decreases)}",
            'severity': 'high'
        })
    
    return changes

def detect_promotional_changes(old_data, new_data):
    """Detect new promotions or offers"""
    changes = []
    
    old_promos = set(old_data.get('promotions', []))
    new_promos = set(new_data.get('promotions', []))
    
    new_promotions = new_promos - old_promos
    
    if new_promotions:
        changes.append({
            'type': 'new_promotion',
            'description': f"New promotions launched: {list(new_promotions)}",
            'severity': 'high'
        })
    
    return changes
```

### 4. Report Generator (reports/report_generator.py)
```python
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

class WarReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 20, 60)  # Crimson red
        self.cell(0, 10, 'BLACK FANG INTELLIGENCE REPORT', ln=True, align='C')
        self.set_text_color(0, 0, 0)  # Back to black
        self.ln(10)

    def threat_level_meter(self, level):
        """Add visual threat level indicator"""
        colors = {'LOW': (0, 255, 0), 'MEDIUM': (255, 165, 0), 'HIGH': (255, 0, 0)}
        color = colors.get(level, (128, 128, 128))
        
        self.set_fill_color(*color)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'THREAT LEVEL: {level}', ln=True, align='C', fill=True)
        self.ln(5)

def generate_war_report(client_name, competitor_data, changes, filename):
    """Generate comprehensive war report PDF"""
    pdf = WarReport()
    pdf.add_page()
    
    # Header section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'CLIENT: {client_name}', ln=True)
    pdf.cell(0, 10, f'REPORT DATE: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True)
    pdf.ln(10)
    
    # Threat level
    threat_level = 'HIGH' if any(c['severity'] == 'high' for c in changes) else 'MEDIUM' if changes else 'LOW'
    pdf.threat_level_meter(threat_level)
    
    # Executive summary
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'EXECUTIVE SUMMARY', ln=True)
    pdf.set_font('Arial', '', 10)
    
    if changes:
        pdf.multi_cell(0, 10, f"Detected {len(changes)} significant competitor moves in the past week. Immediate action recommended.")
    else:
        pdf.multi_cell(0, 10, "No significant competitor changes detected. Continue monitoring.")
    
    pdf.ln(5)
    
    # Detailed findings
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'COMPETITOR INTELLIGENCE', ln=True)
    
    for i, change in enumerate(changes, 1):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, f'{i}. {change["type"].replace("_", " ").upper()}', ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 10, change["description"])
        pdf.ln(3)
    
    # Recommendations
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'RECOMMENDED ACTIONS', ln=True)
    pdf.set_font('Arial', '', 10)
    
    recommendations = generate_recommendations(changes)
    for rec in recommendations:
        pdf.multi_cell(0, 10, f"• {rec}")
        pdf.ln(2)
    
    pdf.output(filename)
    return filename

def generate_recommendations(changes):
    """Generate tactical recommendations based on detected changes"""
    recommendations = []
    
    for change in changes:
        if change['type'] == 'price_decrease':
            recommendations.append("Consider price matching or highlighting superior value proposition")
        elif change['type'] == 'new_promotion':
            recommendations.append("Launch counter-promotional campaign within 48 hours")
        elif change['type'] == 'negative_reviews':
            recommendations.append("Target competitor's service gaps in your marketing messaging")
    
    if not recommendations:
        recommendations.append("Maintain current strategy - no immediate threats detected")
    
    return recommendations
```

### 5. Email Delivery (delivery/email_sender.py)
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

def send_war_report(recipient_email, client_name, report_path, sender_email, sender_password):
    """Send war report via email"""
    
    subject = f"🎯 BLACK FANG Weekly Intelligence Report - {client_name}"
    
    body = f"""
Dear {client_name},

Your weekly competitive intelligence report is attached.

KEY HIGHLIGHTS:
• Competitor monitoring active across all channels
• Real-time threat detection enabled
• Strategic recommendations included

This report contains confidential competitive intelligence. Do not share outside your organization.

Best regards,
Black Fang Intelligence Team

---
"We see what they hide. You win."
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF report
    if os.path.exists(report_path):
        with open(report_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= "BLACK_FANG_Report_{client_name}.pdf"',
            )
            msg.attach(part)
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
```

### 6. Main Execution Script (main.py)
```python
#!/usr/bin/env python3
import json
from datetime import datetime
from scrapers.website_scraper import scrape_static
from scrapers.review_scraper import fetch_google_reviews, analyze_review_trends
from analysis.change_detector import detect_price_changes, detect_promotional_changes
from reports.report_generator import generate_war_report
from delivery.email_sender import send_war_report

def load_config():
    """Load configuration from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def load_old_data():
    """Load previous data for comparison"""
    try:
        with open('data/old_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_new_data(data):
    """Save current data as new baseline"""
    with open('data/new_data.json', 'w') as f:
        json.dump(data, f, indent=2)

def run_intelligence_pipeline():
    """Main intelligence gathering and reporting pipeline"""
    print("🎯 BLACK FANG Intelligence Pipeline Starting...")
    
    # Load configuration
    config = load_config()
    client_name = config['client_name']
    
    # Load old data for comparison
    old_data = load_old_data()
    
    # Gather new intelligence
    print("📡 Gathering competitor intelligence...")
    
    new_data = {}
    
    # Scrape competitor website
    if config.get('competitor_url'):
        website_data = scrape_static(config['competitor_url'])
        new_data.update(website_data)
        print(f"   ✓ Website scraped: {len(website_data.get('prices', []))} prices found")
    
    # Fetch Google reviews
    if config.get('google_place_id') and config.get('google_api_key'):
        reviews = fetch_google_reviews(config['google_place_id'], config['google_api_key'])
        review_analysis = analyze_review_trends(reviews)
        new_data['reviews'] = review_analysis
        print(f"   ✓ Reviews analyzed: {review_analysis['negative_count']} negative reviews")
    
    # Detect changes
    print("🔍 Analyzing competitor moves...")
    changes = []
    
    if old_data:
        price_changes = detect_price_changes(old_data, new_data)
        promo_changes = detect_promotional_changes(old_data, new_data)
        changes.extend(price_changes + promo_changes)
        print(f"   ✓ {len(changes)} significant changes detected")
    else:
        print("   ⚠️ No baseline data - establishing first dataset")
    
    # Generate war report
    print("📊 Generating intelligence report...")
    report_filename = f"reports/BLACK_FANG_Report_{client_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    generate_war_report(client_name, new_data, changes, report_filename)
    print(f"   ✓ Report generated: {report_filename}")
    
    # Send report via email
    if config.get('email'):
        print("📧 Delivering intelligence report...")
        success = send_war_report(
            config['email']['recipient'],
            client_name,
            report_filename,
            config['email']['sender'],
            config['email']['password']
        )
        if success:
            print("   ✓ Report delivered successfully")
        else:
            print("   ❌ Report delivery failed")
    
    # Save current data as baseline for next run
    save_new_data(new_data)
    
    print("🎯 BLACK FANG Intelligence Pipeline Complete!")
    print(f"📈 Status: {len(changes)} threats detected and reported")

if __name__ == "__main__":
    run_intelligence_pipeline()
```

## Deployment Instructions

### 1. Local Setup
```bash
# Clone/download the project
cd blackfang/

# Install dependencies
pip install -r requirements.txt

# Configure your settings
nano config.json

# Run the intelligence pipeline
python main.py
```

### 2. Automation Setup
```bash
# Add to crontab for weekly execution
0 9 * * 1 /usr/bin/python3 /path/to/blackfang/main.py

# Or use GitHub Actions for cloud automation
```

### 3. Scaling Considerations
- Use SQLite → PostgreSQL for larger datasets
- Add Redis for caching frequently accessed data
- Implement rate limiting for web scraping
- Add proxy rotation for large-scale scraping
- Consider Docker containerization for deployment

## Legal & Ethical Considerations
- Only scrape publicly available information
- Respect robots.txt files
- Implement reasonable request delays
- Use proper User-Agent headers
- Never scrape private/authenticated content
- Include clear data source attribution
- Maintain client data confidentiality with NDAs