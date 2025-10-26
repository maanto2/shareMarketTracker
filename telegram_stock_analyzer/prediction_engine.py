#!/usr/bin/env python3
"""
Prediction Engine
Generates BUY/SELL/HOLD recommendations based on technical and sentiment analysis
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

class PredictionEngine:
    def __init__(self):
        """Initialize prediction engine with scoring weights"""
        # Scoring weights for different factors
        self.weights = {
            'technical': 0.6,      # 60% weight to technical analysis
            'sentiment': 0.3,      # 30% weight to sentiment analysis
            'fundamental': 0.1     # 10% weight to fundamental data
        }
        
        # Confidence thresholds
        self.confidence_thresholds = {
            'high': 80,      # High confidence recommendation
            'medium': 60,    # Medium confidence recommendation
            'low': 40        # Low confidence recommendation
        }
    
    def get_prediction(self, analysis: Dict) -> Dict:
        """
        Generate trading prediction based on comprehensive analysis
        
        Args:
            analysis: Complete stock analysis dictionary
            
        Returns:
            Dictionary with recommendation, confidence, and reasoning
        """
        try:
            # Extract analysis components
            technical = analysis.get('technical_analysis', {})
            sentiment = analysis.get('sentiment_analysis', {})
            market_data = analysis.get('market_data', {})
            
            # Calculate individual scores
            technical_score = self._calculate_technical_score(technical)
            sentiment_score = self._calculate_sentiment_score(sentiment)
            fundamental_score = self._calculate_fundamental_score(market_data, analysis.get('current_price', 0))
            
            # Calculate weighted overall score
            overall_score = (
                technical_score * self.weights['technical'] +
                sentiment_score * self.weights['sentiment'] +
                fundamental_score * self.weights['fundamental']
            )
            
            # Generate recommendation
            recommendation = self._generate_recommendation(overall_score)
            
            # Calculate confidence
            confidence = self._calculate_confidence(technical, sentiment, overall_score)
            
            # Generate detailed reasoning
            reasoning = self._generate_reasoning(
                technical, sentiment, market_data,
                technical_score, sentiment_score, fundamental_score,
                overall_score
            )
            
            return {
                'recommendation': {
                    'action': recommendation,
                    'confidence': confidence,
                    'reason': reasoning
                },
                'scores': {
                    'overall': overall_score,
                    'technical': technical_score,
                    'sentiment': sentiment_score,
                    'fundamental': fundamental_score
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'recommendation': {
                    'action': 'HOLD',
                    'confidence': 0,
                    'reason': f'Analysis failed: {str(e)}'
                },
                'scores': {
                    'overall': 0,
                    'technical': 0,
                    'sentiment': 0,
                    'fundamental': 0
                },
                'error': str(e)
            }
    
    def _calculate_technical_score(self, technical: Dict) -> float:
        """Calculate technical analysis score (-100 to +100)"""
        if not technical or technical.get('error'):
            return 0
        
        score = 0
        
        # Price momentum (40% of technical score)
        day_change = technical.get('day_change_pct', 0)
        week_change = technical.get('week_change_pct', 0)
        month_change = technical.get('month_change_pct', 0)
        
        # Recent performance is more important
        momentum_score = (day_change * 0.5 + week_change * 0.3 + month_change * 0.2)
        score += momentum_score * 0.4
        
        # RSI analysis (25% of technical score)
        rsi = technical.get('rsi', 50)
        if rsi < 30:  # Oversold - bullish
            rsi_score = 20
        elif rsi > 70:  # Overbought - bearish
            rsi_score = -20
        else:  # Neutral
            rsi_score = 0
        score += rsi_score * 0.25
        
        # Moving average position (20% of technical score)
        price_vs_ma20 = technical.get('price_vs_ma20', 0)
        price_vs_ma50 = technical.get('price_vs_ma50', 0)
        
        ma_score = 0
        if price_vs_ma20 > 2 and price_vs_ma50 > 2:  # Above both MAs
            ma_score = 15
        elif price_vs_ma20 > 0 and price_vs_ma50 > 0:  # Above both but close
            ma_score = 10
        elif price_vs_ma20 < -2 and price_vs_ma50 < -2:  # Below both MAs
            ma_score = -15
        elif price_vs_ma20 < 0 and price_vs_ma50 < 0:  # Below both but close
            ma_score = -10
        
        score += ma_score * 0.2
        
        # Volume analysis (15% of technical score)
        volume_ratio = technical.get('volume_ratio', 1)
        if volume_ratio > 2:  # High volume - strong signal
            volume_score = 10
        elif volume_ratio > 1.5:  # Above average volume
            volume_score = 5
        elif volume_ratio < 0.5:  # Low volume - weak signal
            volume_score = -5
        else:
            volume_score = 0
        
        score += volume_score * 0.15
        
        # Cap the score at reasonable bounds
        return max(-100, min(100, score))
    
    def _calculate_sentiment_score(self, sentiment: Dict) -> float:
        """Calculate sentiment analysis score (-100 to +100)"""
        if not sentiment or sentiment.get('error'):
            return 0
        
        overall_sentiment = sentiment.get('overall_sentiment', 'neutral')
        overall_score = sentiment.get('overall_score', 0)
        confidence = sentiment.get('confidence', 0)
        articles_count = sentiment.get('articles_analyzed', 0)
        
        # Base score from sentiment
        if overall_sentiment == 'positive':
            base_score = 30
        elif overall_sentiment == 'negative':
            base_score = -30
        else:
            base_score = 0
        
        # Adjust based on sentiment strength
        score_multiplier = min(abs(overall_score) / 2, 2)  # Cap at 2x
        adjusted_score = base_score * score_multiplier
        
        # Adjust based on confidence
        confidence_multiplier = confidence / 100
        final_score = adjusted_score * confidence_multiplier
        
        # Bonus for more articles (more reliable)
        if articles_count >= 5:
            final_score *= 1.2
        elif articles_count >= 3:
            final_score *= 1.1
        elif articles_count < 2:
            final_score *= 0.7
        
        return max(-100, min(100, final_score))
    
    def _calculate_fundamental_score(self, market_data: Dict, current_price: float) -> float:
        """Calculate fundamental analysis score (-100 to +100)"""
        if not market_data:
            return 0
        
        score = 0
        
        # P/E Ratio analysis
        pe_ratio = market_data.get('pe_ratio', 0)
        if pe_ratio > 0:
            if pe_ratio < 15:  # Undervalued
                score += 20
            elif pe_ratio > 30:  # Overvalued
                score -= 20
            # Neutral for PE between 15-30
        
        # Market cap consideration (large caps are generally more stable)
        market_cap = market_data.get('market_cap', 0)
        if market_cap > 100e9:  # Large cap (>100B)
            score += 5
        elif market_cap < 2e9:  # Small cap (<2B) - more risky
            score -= 5
        
        # Sector considerations (basic scoring)
        sector = market_data.get('sector', '').lower()
        growth_sectors = ['technology', 'healthcare', 'consumer discretionary']
        defensive_sectors = ['utilities', 'consumer staples', 'real estate']
        
        if any(growth_sector in sector for growth_sector in growth_sectors):
            score += 5
        elif any(defensive_sector in sector for defensive_sector in defensive_sectors):
            score += 2  # Stable but less growth potential
        
        return max(-100, min(100, score))
    
    def _generate_recommendation(self, overall_score: float) -> str:
        """Generate BUY/SELL/HOLD recommendation based on overall score"""
        if overall_score > 30:
            return 'BUY'
        elif overall_score < -30:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _calculate_confidence(self, technical: Dict, sentiment: Dict, overall_score: float) -> float:
        """Calculate confidence level for the recommendation"""
        confidence_factors = []
        
        # Technical analysis confidence
        if technical and not technical.get('error'):
            tech_confidence = 70  # Base confidence for technical analysis
            
            # Higher confidence if multiple indicators align
            indicators_positive = 0
            indicators_negative = 0
            
            # Check day change
            day_change = technical.get('day_change_pct', 0)
            if day_change > 2:
                indicators_positive += 1
            elif day_change < -2:
                indicators_negative += 1
            
            # Check RSI
            rsi = technical.get('rsi', 50)
            if rsi < 30 or rsi > 70:  # Strong RSI signal
                if rsi < 30:
                    indicators_positive += 1
                else:
                    indicators_negative += 1
            
            # Check volume
            volume_ratio = technical.get('volume_ratio', 1)
            if volume_ratio > 1.5:
                tech_confidence += 10
            
            # Alignment bonus
            if indicators_positive >= 2 and indicators_negative == 0:
                tech_confidence += 15
            elif indicators_negative >= 2 and indicators_positive == 0:
                tech_confidence += 15
            
            confidence_factors.append(tech_confidence)
        
        # Sentiment analysis confidence
        if sentiment and not sentiment.get('error'):
            sent_confidence = sentiment.get('confidence', 0)
            articles_analyzed = sentiment.get('articles_analyzed', 0)
            
            # Adjust based on number of articles
            if articles_analyzed >= 5:
                sent_confidence *= 1.2
            elif articles_analyzed < 2:
                sent_confidence *= 0.6
            
            confidence_factors.append(min(sent_confidence, 100))
        
        # Overall score strength
        score_confidence = min(abs(overall_score) * 1.5, 100)
        confidence_factors.append(score_confidence)
        
        # Calculate weighted average
        if confidence_factors:
            final_confidence = np.mean(confidence_factors)
        else:
            final_confidence = 50  # Neutral confidence
        
        return max(0, min(100, final_confidence))
    
    def _generate_reasoning(self, technical: Dict, sentiment: Dict, market_data: Dict,
                          technical_score: float, sentiment_score: float, fundamental_score: float,
                          overall_score: float) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        
        # Technical reasoning
        if technical and not technical.get('error'):
            day_change = technical.get('day_change_pct', 0)
            rsi = technical.get('rsi', 50)
            volume_ratio = technical.get('volume_ratio', 1)
            
            if technical_score > 20:
                reasons.append("Strong technical indicators")
                if day_change > 3:
                    reasons.append(f"strong daily momentum (+{day_change:.1f}%)")
                if rsi < 30:
                    reasons.append("RSI indicates oversold condition")
                if volume_ratio > 2:
                    reasons.append("unusually high trading volume")
            elif technical_score < -20:
                reasons.append("Weak technical indicators")
                if day_change < -3:
                    reasons.append(f"negative daily momentum ({day_change:.1f}%)")
                if rsi > 70:
                    reasons.append("RSI indicates overbought condition")
            else:
                reasons.append("Mixed technical signals")
        
        # Sentiment reasoning
        if sentiment and not sentiment.get('error'):
            overall_sentiment = sentiment.get('overall_sentiment', 'neutral')
            articles_count = sentiment.get('articles_analyzed', 0)
            
            if sentiment_score > 15:
                reasons.append(f"positive news sentiment from {articles_count} articles")
            elif sentiment_score < -15:
                reasons.append(f"negative news sentiment from {articles_count} articles")
            elif articles_count > 0:
                reasons.append(f"neutral news sentiment from {articles_count} articles")
        
        # Fundamental reasoning
        if market_data and fundamental_score != 0:
            pe_ratio = market_data.get('pe_ratio', 0)
            sector = market_data.get('sector', '')
            
            if fundamental_score > 10:
                reasons.append("favorable fundamental metrics")
                if pe_ratio > 0 and pe_ratio < 15:
                    reasons.append(f"attractive P/E ratio ({pe_ratio:.1f})")
            elif fundamental_score < -10:
                reasons.append("concerning fundamental metrics")
                if pe_ratio > 30:
                    reasons.append(f"high P/E ratio ({pe_ratio:.1f})")
            
            if sector:
                reasons.append(f"operates in {sector.lower()} sector")
        
        # Overall reasoning
        if overall_score > 50:
            opening = "Multiple strong positive factors align"
        elif overall_score > 30:
            opening = "Several positive factors outweigh negatives"
        elif overall_score < -50:
            opening = "Multiple concerning factors align"
        elif overall_score < -30:
            opening = "Several negative factors outweigh positives"
        else:
            opening = "Mixed signals from various indicators"
        
        # Combine all reasons
        if reasons:
            reason_text = opening + ": " + ", ".join(reasons[:4])  # Limit to top 4 reasons
        else:
            reason_text = opening
        
        return reason_text.capitalize() + "."

def main():
    """Test function"""
    # Mock analysis data for testing
    mock_analysis = {
        'symbol': 'AAPL',
        'current_price': 175.43,
        'technical_analysis': {
            'day_change_pct': 2.3,
            'week_change_pct': 5.7,
            'month_change_pct': -1.2,
            'rsi': 65,
            'volume_ratio': 1.8,
            'price_vs_ma20': 3.2,
            'price_vs_ma50': 1.8
        },
        'sentiment_analysis': {
            'overall_sentiment': 'positive',
            'overall_score': 2.1,
            'confidence': 75,
            'articles_analyzed': 6
        },
        'market_data': {
            'pe_ratio': 25.4,
            'market_cap': 2.8e12,
            'sector': 'Technology'
        }
    }
    
    # Test prediction engine
    engine = PredictionEngine()
    prediction = engine.get_prediction(mock_analysis)
    
    print("🔮 PREDICTION ENGINE TEST")
    print("=" * 40)
    print(f"📊 Overall Score: {prediction['scores']['overall']:.1f}")
    print(f"🎯 Recommendation: {prediction['recommendation']['action']}")
    print(f"📈 Confidence: {prediction['recommendation']['confidence']:.1f}%")
    print(f"💡 Reasoning: {prediction['recommendation']['reason']}")
    print("\n📊 Detailed Scores:")
    print(f"  Technical: {prediction['scores']['technical']:.1f}")
    print(f"  Sentiment: {prediction['scores']['sentiment']:.1f}")
    print(f"  Fundamental: {prediction['scores']['fundamental']:.1f}")

if __name__ == "__main__":
    main()