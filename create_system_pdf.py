#!/usr/bin/env python3
"""
Generate PDF Documentation for Market Analysis System Timeline
Creates a comprehensive PDF report with system architecture and timeline breakdown
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def create_market_system_pdf():
    """Create comprehensive PDF documentation"""
    
    # Create PDF file
    filename = f"Market_Analysis_System_Timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        spaceBefore=20,
        textColor=colors.darkgreen
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        spaceBefore=15,
        textColor=colors.darkred
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    # Story content
    story = []
    
    # Title page
    story.append(Paragraph("📊 MARKET ANALYSIS SYSTEM", title_style))
    story.append(Paragraph("Timeline Breakdown & Architecture Guide", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    
    # System overview
    story.append(Paragraph("🏗️ System Overview", heading_style))
    overview_text = """
    This comprehensive market intelligence platform combines real-time news monitoring with 
    advanced sentiment analysis to provide actionable trading insights. The system operates 
    continuously with multiple parallel processes, delivering both instant alerts and 
    comprehensive market reports via Telegram notifications.
    """
    story.append(Paragraph(overview_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Timeline breakdown table
    story.append(Paragraph("⏰ SENTIMENT ANALYSIS FREQUENCY", heading_style))
    
    # Create frequency table
    frequency_data = [
        ['Component', 'Frequency', 'Scope', 'Method', 'Output'],
        ['🧠 Comprehensive Analysis', 'Every 4 hours', 'Top 10-25 stocks', 'NewsAPI + Advanced scoring', 'BUY/SELL recommendations'],
        ['⚡ Quick Assessment', 'Every 5 minutes', 'Breaking news only', 'Keyword matching', 'Instant alerts'],
        ['📈 Full Market Analysis', 'On-demand', 'All monitored stocks', 'NewsAPI + Full analysis', 'Complete reports'],
        ['📰 RSS Monitoring', 'Every 5 minutes', '26+ stock symbols', 'RSS feed parsing', 'Real-time news alerts'],
        ['📅 Earnings Calendar', 'Every 4 hours', 'Top performers', 'yfinance + sentiment', 'Earnings with BUY/SELL']
    ]
    
    frequency_table = Table(frequency_data, colWidths=[2.2*inch, 1.3*inch, 1.5*inch, 1.8*inch, 1.5*inch])
    frequency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(frequency_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Detailed workflow
    story.append(Paragraph("🔄 SYSTEM WORKFLOWS", heading_style))
    
    story.append(Paragraph("1. Real-Time News Monitoring (Continuous)", subheading_style))
    workflow1_text = """
    RSS Feed Check (every 5 min) → Keyword Matching (26+ symbols) → 
    Urgency Scoring (1-10 scale) → Quick Sentiment Analysis → 
    BUY/SELL Assessment → Instant Telegram Alert
    """
    story.append(Paragraph(workflow1_text, normal_style))
    
    story.append(Paragraph("2. Comprehensive Market Analysis (Every 4 hours)", subheading_style))
    workflow2_text = """
    S&P 500 Data Pull → Top Performers Analysis → Earnings Calendar Check → 
    Advanced Sentiment Analysis → Trading Recommendations → 
    Comprehensive Telegram Report with BUY/SELL indicators
    """
    story.append(Paragraph(workflow2_text, normal_style))
    
    story.append(Paragraph("3. Parallel System Operation", subheading_style))
    workflow3_text = """
    Thread 1: News Monitor (continuous 5-min cycles)
    Thread 2: Market Analysis (4-hour comprehensive cycles)
    Main Thread: System coordination, error handling & user interface
    """
    story.append(Paragraph(workflow3_text, normal_style))
    
    # System components
    story.append(PageBreak())
    story.append(Paragraph("🎯 CORE SYSTEM COMPONENTS", heading_style))
    
    # Components table
    components_data = [
        ['Component', 'File', 'Primary Function', 'Update Frequency'],
        ['News Monitor', 'flash_news_monitor.py', 'Real-time RSS monitoring & alerts', 'Every 5 minutes'],
        ['Market Orchestrator', 'market_orchestrator.py', 'S&P 500 analysis & reports', 'Every 4 hours'],
        ['Telegram Bot', 'telegram_bot.py', 'Enhanced message formatting', 'Real-time'],
        ['Sentiment Analyzer', 'sentiment_analyzer.py', 'News sentiment & BUY/SELL logic', 'Per analysis'],
        ['Unified System', 'unified_market_system.py', 'Parallel system coordination', 'Continuous'],
        ['Config Loader', 'config_loader.py', 'Secure credential management', 'On startup']
    ]
    
    components_table = Table(components_data, colWidths=[2*inch, 2.2*inch, 2.5*inch, 1.5*inch])
    components_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(components_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Trading recommendations
    story.append(Paragraph("📈 TRADING RECOMMENDATION SYSTEM", heading_style))
    
    recommendations_data = [
        ['Signal', 'Criteria', 'Confidence', 'Emoji', 'Action'],
        ['STRONG BUY', 'Score >1.5, Positive', '>70%', '🟢🟢', 'High conviction buy'],
        ['BUY', 'Score >0.5, Positive', '>70%', '🟢', 'Moderate buy'],
        ['WEAK BUY', 'Score >1.0, Positive', '50-70%', '🟡', 'Cautious buy'],
        ['STRONG SELL', 'Score <-1.5, Negative', '>70%', '🔴🔴', 'High conviction sell'],
        ['SELL', 'Score <-0.5, Negative', '>70%', '🔴', 'Moderate sell'],
        ['WEAK SELL', 'Score <-1.0, Negative', '50-70%', '🟠', 'Cautious sell'],
        ['HOLD', 'Mixed/Neutral', '<50%', '⚪', 'Monitor & hold'],
    ]
    
    recommendations_table = Table(recommendations_data, colWidths=[1.3*inch, 1.8*inch, 1.2*inch, 0.8*inch, 1.4*inch])
    recommendations_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(recommendations_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Monitored assets
    story.append(Paragraph("📊 MONITORED ASSETS", heading_style))
    
    assets_text = """
    The system monitors 26+ stock symbols across major sectors:
    
    • Tech Giants: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA
    • Financial: JPM, V, MA, UNH  
    • Consumer: PG, HD, DIS, NFLX
    • Software: CRM, ADBE, PYPL, INTC, CSCO
    • Healthcare: JNJ, PFE
    • ETFs: SPY, QQQ, IWM, VIX
    
    News sources include Yahoo Finance RSS, MarketWatch, CNBC, and optional NewsAPI integration.
    """
    story.append(Paragraph(assets_text, normal_style))
    
    # Configuration options
    story.append(Paragraph("⚙️ CONFIGURATION OPTIONS", heading_style))
    
    config_text = """
    The system offers flexible configuration through JSON files and environment variables:
    
    • Monitoring intervals (default: 5 minutes for news, 4 hours for analysis)
    • Symbol lists and keyword filters
    • Urgency thresholds and confidence levels
    • Telegram notification settings
    • API keys and rate limiting
    • Security through .env file separation
    """
    story.append(Paragraph(config_text, normal_style))
    
    # Usage instructions
    story.append(PageBreak())
    story.append(Paragraph("🚀 SYSTEM USAGE", heading_style))
    
    usage_data = [
        ['Command', 'Purpose', 'Components Active'],
        ['python unified_market_system.py', 'Complete system (Recommended)', 'News Monitor + Market Analysis'],
        ['python start_news_monitor.py', 'Real-time alerts only', 'News Monitor only'],
        ['python market_orchestrator.py', 'Analysis reports only', 'Market Analysis only'],
        ['python launch_system.py', 'Interactive menu', 'User choice'],
    ]
    
    usage_table = Table(usage_data, colWidths=[2.5*inch, 2.5*inch, 2.2*inch])
    usage_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(usage_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_text = f"""
    📋 Document generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    🔗 GitHub Repository: https://github.com/maanto2/shareMarketTracker
    📧 System Status: Fully operational with BUY/SELL recommendations
    """
    story.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(story)
    
    return filename

if __name__ == "__main__":
    try:
        filename = create_market_system_pdf()
        print(f"✅ PDF Documentation Created Successfully!")
        print(f"📄 File: {filename}")
        print(f"📁 Location: {os.path.abspath(filename)}")
        print(f"📊 Content: Comprehensive system timeline and architecture guide")
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()