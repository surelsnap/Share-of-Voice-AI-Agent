"""
Document Generator
Creates the two-pager document with tech stack and findings/recommendations
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict
import os


class DocumentGenerator:
    """Generate two-pager PDF document"""
    
    def __init__(self, config):
        self.config = config
        self.output_file = f"{config.OUTPUT_DIR}/two_pager_report.pdf"
    
    def generate_two_pager(self, results: Dict):
        """Generate the two-pager document"""
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for the 'Flowable' objects
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        # PAGE 1: Tech Stack
        story.append(Paragraph("Atomberg SoV Analysis Agent", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Technical Documentation", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Tech Stack Section
        story.append(Paragraph("Technology Stack", subheading_style))
        
        tech_stack_data = [
            ['Component', 'Technology/Tool'],
            ['Language', 'Python 3.8+'],
            ['Search Engines', 'Google Custom Search API, YouTube Search API'],
            ['Data Processing', 'Pandas, NumPy'],
            ['Sentiment Analysis', 'VADER Sentiment, TextBlob'],
            ['Visualization', 'Matplotlib, Seaborn'],
            ['PDF Generation', 'ReportLab'],
            ['Web Scraping', 'BeautifulSoup4, Requests'],
            ['Data Storage', 'JSON, CSV']
        ]
        
        tech_table = Table(tech_stack_data, colWidths=[2*inch, 4*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(tech_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Architecture Section
        story.append(Paragraph("System Architecture", subheading_style))
        architecture_text = """
        The AI agent follows a modular architecture with the following components:
        <br/><br/>
        <b>1. Search Engines Module:</b> Handles searches across Google (secondary) and YouTube (primary) platforms with enhanced engagement metrics and comment collection.
        <br/><br/>
        <b>2. SoV Calculator:</b> Computes Share of Voice using formula: (0.4 × Presence) + (0.3 × Engagement) + (0.2 × Sentiment) + (0.1 × Dominance).
        <br/><br/>
        <b>3. Sentiment Analyzer:</b> Uses VADER and TextBlob to analyze sentiment and calculate Share of Positive Voice.
        <br/><br/>
        <b>4. Cross-Keyword Analyzer:</b> Identifies content gaps, keyword associations, and opportunity areas across multiple search terms.
        <br/><br/>
        <b>5. Insights Generator:</b> Processes analysis results to generate actionable insights and recommendations with content gap analysis.
        <br/><br/>
        <b>6. Document Generator:</b> Creates comprehensive reports and visualizations.
        """
        story.append(Paragraph(architecture_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Key Features
        story.append(Paragraph("Key Features", subheading_style))
        features_text = """
        • Multi-platform search (YouTube primary, Google secondary)
        <br/>• Enhanced SoV calculation: Presence (40%) + Engagement (30%) + Sentiment (20%) + Dominance (10%)
        <br/>• Cross-keyword analysis with content gap identification
        <br/>• Engagement normalization and ranking dominance scoring
        <br/>• Sentiment analysis with positive voice tracking
        <br/>• Automated keyword strategy recommendations
        <br/>• Visualizations and comprehensive reporting
        """
        story.append(Paragraph(features_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Links Section
        story.append(Paragraph("Additional Resources", subheading_style))
        links_text = """
        <b>GitHub Repository:</b> <link href='https://github.com/yourusername/atomberg-sov-agent' color='blue'>github.com/yourusername/atomberg-sov-agent</link>
        <br/><br/>
        <b>Code Structure:</b>
        <br/>• main.py - Entry point
        <br/>• sov_agent.py - Main agent orchestrator
        <br/>• search_engines.py - Platform search with enhanced YouTube metrics
        <br/>• sov_calculator.py - SoV calculations with 4-metric formula
        <br/>• sentiment_analyzer.py - Sentiment analysis engine
        <br/>• cross_keyword_analyzer.py - Cross-keyword analysis and gap identification
        <br/>• insights_generator.py - Insights with content gap analysis
        <br/>• document_generator.py - Enhanced report generation
        <br/><br/>
        <b>Setup Instructions:</b>
        <br/>1. Install dependencies: pip install -r requirements.txt
        <br/>2. Configure API keys in .env file (optional for demo mode)
        <br/>3. Run: python main.py
        """
        story.append(Paragraph(links_text, body_style))
        
        # Page Break
        story.append(PageBreak())
        
        # PAGE 2: Findings and Recommendations
        story.append(Paragraph("Atomberg SoV Analysis", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Findings & Recommendations", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Overall SoV Summary
        if "overall_sov" in results:
            overall = results["overall_sov"]
            sov_percentage = overall.get("sov_percentage", {})
            brand_sov = sov_percentage.get(self.config.BRAND_NAME, 0)
            
            story.append(Paragraph("Executive Summary", subheading_style))
            summary_text = f"""
            Analysis of Share of Voice (SoV) across multiple platforms reveals that <b>Atomberg has {brand_sov:.1f}% overall Share of Voice</b> 
            when searching for keywords related to smart fans. The analysis covered {overall.get('platform_count', 0)} platform(s) 
            and analyzed mentions, engagement, and sentiment across {len(self.config.SEARCH_KEYWORDS)} keyword variations.
            """
            story.append(Paragraph(summary_text, body_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Platform-wise Findings
        story.append(Paragraph("Platform-wise Analysis", subheading_style))
        
        if "platform_sov" in results:
            for platform, data in results["platform_sov"].items():
                sov_metrics = data.get("sov_metrics", {})
                weighted_sov = sov_metrics.get("weighted_sov", {})
                brand_sov = weighted_sov.get(self.config.BRAND_NAME, 0)
                
                # Find top competitor
                competitor_sovs = {
                    comp: weighted_sov.get(comp, 0) 
                    for comp in self.config.COMPETITOR_BRANDS
                }
                top_competitor = max(competitor_sovs.items(), key=lambda x: x[1]) if competitor_sovs else ("N/A", 0)
                
                platform_text = f"""
                <b>{platform.capitalize()}:</b> Atomberg's SoV is {brand_sov:.1f}%. 
                Top competitor ({top_competitor[0]}) has {top_competitor[1]:.1f}% SoV.
                """
                story.append(Paragraph(platform_text, body_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Cross-Keyword Analysis
        if "cross_keyword_analysis" in results:
            cross_kw = results["cross_keyword_analysis"]
            story.append(Paragraph("Cross-Keyword Analysis", subheading_style))
            
            # Content Gaps
            gaps = cross_kw.get("content_gaps", [])
            if gaps:
                gaps_text = "<b>Content Gaps Identified:</b><br/><br/>"
                for i, gap in enumerate(gaps[:3], 1):  # Top 3 gaps
                    gaps_text += f"{i}. <b>{gap['keyword']}</b>: Atomberg {gap['atomberg_sov']:.1f}% vs {gap['top_competitor']} {gap['competitor_sov']:.1f}% (Gap: {gap['gap']:.1f}%)<br/>"
                story.append(Paragraph(gaps_text, body_style))
                story.append(Spacer(1, 0.1*inch))
            
            # Opportunity Areas
            opportunities = cross_kw.get("opportunity_areas", [])
            if opportunities:
                opp_text = "<b>Opportunity Areas:</b><br/><br/>"
                for opp in opportunities:
                    priority_icon = "🔴" if opp.get("priority") == "high" else "🟡"
                    opp_text += f"{priority_icon} <b>{opp['area']}</b>: {opp['recommendation']}<br/><br/>"
                story.append(Paragraph(opp_text, body_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Sentiment Analysis
        if "platform_sov" in results:
            story.append(Paragraph("Sentiment Analysis", subheading_style))
            sentiment_text = ""
            for platform, data in list(results["platform_sov"].items())[:2]:  # Top 2 platforms
                sentiment = data.get("sentiment", {})
                sentiment_stats = sentiment.get("sentiment_stats", {})
                brand_sentiment = sentiment_stats.get(self.config.BRAND_NAME, {})
                
                if brand_sentiment:
                    positive_ratio = brand_sentiment.get("positive_ratio", 0) * 100
                    sentiment_text += f"<b>{platform.capitalize()}:</b> {positive_ratio:.1f}% positive mentions<br/>"
            
            if sentiment_text:
                story.append(Paragraph(sentiment_text, body_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        story.append(Paragraph("Key Recommendations", subheading_style))
        
        if "insights" in results:
            # Group insights by type
            content_gap_insights = [i for i in results["insights"] if i.get("type") == "content_gap"]
            opportunity_insights = [i for i in results["insights"] if i.get("type") == "opportunity_area"]
            other_insights = [i for i in results["insights"] if i.get("type") not in ["content_gap", "opportunity_area"]]
            
            recommendations_text = ""
            
            # Content gap recommendations
            if content_gap_insights:
                recommendations_text += "<b>Content Creation Priorities:</b><br/>"
                for i, insight in enumerate(content_gap_insights[:2], 1):
                    recommendations_text += f"{i}. {insight.get('recommendation', '')}<br/><br/>"
            
            # Opportunity area recommendations
            if opportunity_insights:
                recommendations_text += "<b>Strategic Opportunities:</b><br/>"
                for i, insight in enumerate(opportunity_insights[:2], 1):
                    recommendations_text += f"{i}. {insight.get('recommendation', '')}<br/><br/>"
            
            # Other key recommendations
            if other_insights:
                recommendations_text += "<b>General Recommendations:</b><br/>"
                for i, insight in enumerate(other_insights[:3], 1):
                    rec = insight.get("recommendation", "")
                    if rec:
                        recommendations_text += f"{i}. {rec}<br/><br/>"
            
            if recommendations_text:
                story.append(Paragraph(recommendations_text, body_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Keyword Strategy
        story.append(Paragraph("Keyword Strategy", subheading_style))
        keyword_strategy_text = """
        <b>Strengths:</b> Leverage keywords where Atomberg currently leads in SoV.
        <br/><br/>
        <b>Opportunities:</b> Focus content creation on keywords with identified gaps (>10% SoV difference).
        <br/><br/>
        <b>Threats:</b> Monitor competitor activity in high-value keywords and respond with targeted content.
        <br/><br/>
        <b>Action Plan:</b> Create content calendar prioritizing gap keywords, with emphasis on technical content (BLDC, energy efficiency) and commercial content (smart features, WiFi connectivity).
        """
        story.append(Paragraph(keyword_strategy_text, body_style))
        
        # Build PDF
        doc.build(story)
        print(f"✓ Generated two-pager document: {self.output_file}")

