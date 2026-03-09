---
title: "Decoding Market Patterns: A Nobel Prize-Inspired Trading Indicator for MetaTrader 5 (edited)"
url: https://medium.com/p/e46a1ed62583
---

# Decoding Market Patterns: A Nobel Prize-Inspired Trading Indicator for MetaTrader 5 (edited)

[Original](https://medium.com/p/e46a1ed62583)

Member-only story

# Decoding Market Patterns: A Nobel Prize-Inspired Trading Indicator for MetaTrader 5 (edited)

[![Javier Santiago Gastón de Iriarte Cabrera](https://miro.medium.com/v2/resize:fill:64:64/1*WgVCI2ExLvGojne7AfMXGQ.jpeg)](/@jsgastoniriartecabrera?source=post_page---byline--e46a1ed62583---------------------------------------)

[Javier Santiago Gastón de Iriarte Cabrera](/@jsgastoniriartecabrera?source=post_page---byline--e46a1ed62583---------------------------------------)

33 min read

·

Jan 17, 2026

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

## How Physics Won the 2024 Nobel Prize and Revolutionized Technical Analysis

\*\*\* Edited to add optimized versions that use less RAM.\*\*\*

Press enter or click to view image in full size

![]()

The 2024 Nobel Prize in Physics awarded to Geoffrey Hinton and John Hopfield for their groundbreaking work in neural networks didn’t just advance artificial intelligence. It sparked a revolution in how we analyze complex systems, including financial markets. Their research on pattern recognition and adaptive learning systems has inspired a new generation of trading tools that can identify market structures with unprecedented accuracy.

Today, we’re diving deep into a sophisticated MetaTrader 5 indicator that applies these principles to real-time market analysis. This isn’t just another arrow indicator. It’s a comprehensive system that identifies candle patterns, calculates optimal entry zones using Fibonacci retracements, and provides actionable trading signals based on market structure analysis.

## The Core Philosophy: Pattern Recognition Meets Market Structure

Press enter or click to view image in full size

![]()

Traditional technical analysis relies heavily on subjective interpretation. A trader might see a bullish pattern where another sees consolidation. This indicator eliminates that ambiguity by applying systematic pattern classification inspired by neural network decision trees.

The system analyzes three consecutive swing points (highs and lows) to create an eight-pattern classification system. Each pattern receives a strength score and directional bias, similar to how neural networks assign confidence scores to their predictions.

## Understanding the HLC Pattern System

The indicator uses a brilliant yet simple notation: HLC stands for Higher-Lower-Close analysis. By examining whether recent swing highs and lows are making higher or lower patterns, the system can classify market structure into eight distinct patterns:

**HHH (Higher High, Higher Low, continued)** represents the strongest bullish momentum, scoring up to 95% strength. This is your textbook uptrend with consistent higher highs and higher lows across three swing points.

**LLL (Lower Low, Lower High, continued)** mirrors this on the bearish side, indicating strong downward momentum with pattern strength reaching 95%.

**HHL and LHL patterns** represent strong bullish structures with minor pullbacks, scoring between 75–85% strength. These are excellent continuation patterns.

**LLH and LHL patterns** indicate bearish structures with varying degrees of strength, perfect for identifying short opportunities in downtrends.

**RANGE patterns** occur when the market lacks clear directional structure, receiving the lowest strength score of 20%.

## The Advanced Detection Engine

Let’s examine how the indicator identifies these patterns in the code. The core detection happens in the `AnalyzeCandlePattern()` function:

```
void AnalyzeCandlePattern()  
{  
   // Reset state for fresh analysis  
   m_structure.isBullish = false;  
   m_structure.isBearish = false;  
     
   // Validate we have sufficient swing data  
   if(m_structure.lastHigh == 0 || m_structure.prevHigh == 0 ||   
      m_structure.lastLow == 0 || m_structure.prevLow == 0)  
   {  
      m_structure.pattern = PATTERN_RANGE;  
      m_structure.patternName = "RANGE";  
      m_structure.patternStrength = 20;  
      return;  
   }  
     
   // Compare recent swings to classify pattern  
   bool HH = m_structure.lastHigh > m_structure.prevHigh;   // Higher high?  
   bool HL = m_structure.lastHigh < m_structure.prevHigh;   // Lower high?  
   bool HiL = m_structure.lastLow > m_structure.prevLow;    // Higher low?  
   bool LoL = m_structure.lastLow < m_structure.prevLow;    // Lower low?  
     
   // Pattern classification with strength scoring  
   if(HH && HiL)  // Both making higher points  
   {  
      if(m_structure.prevHigh > m_structure.prev2High &&   
         m_structure.prevLow > m_structure.prev2Low)  
      {  
         // Three consecutive bullish swings = strongest pattern  
         m_structure.pattern = PATTERN_HHH;  
         m_structure.patternName = "HHH";  
         m_structure.patternStrength = 95;  
         m_structure.isBullish = true;  
         m_structure.consecutiveBullish = 3;  
      }  
   }  
}
```

This approach embodies the Nobel Prize-winning concept of hierarchical feature detection. Just as Hopfield networks recognize patterns through interconnected nodes, this code evaluates multiple conditions simultaneously to arrive at a classification.

## Fibonacci Zones: Finding the Sweet Spot

One of the indicator’s most powerful features is its dynamic Fibonacci zone calculation. Rather than drawing static Fibonacci levels that require manual adjustment, the system automatically identifies the relevant swing range and calculates optimal retracement zones.

The magic happens in the `CalculateFibonacciZones()` function:

```
void CalculateFibonacciZones()  
{  
   // Establish dynamic support and resistance from recent swings  
   m_structure.dynamicSupport = MathMin(m_structure.lastLow, m_structure.prevLow);  
   m_structure.dynamicResistance = MathMax(m_structure.lastHigh, m_structure.prevHigh);  
     
   double range = m_structure.dynamicResistance - m_structure.dynamicSupport;  
     
   if(m_structure.isBullish)  
   {  
      // Calculate retracement zones from resistance downward  
      m_structure.fib_382 = m_structure.dynamicResistance - (range * 0.382);  
      m_structure.fib_500 = m_structure.dynamicResistance - (range * 0.500);  
      m_structure.fib_618 = m_structure.dynamicResistance - (range * 0.618);  
      m_structure.fib_786 = m_structure.dynamicResistance - (range * 0.786);  
   }  
}
```

These Fibonacci levels divide the market into four distinct zones: Optimal (38.2%-50%), Acceptable (50%-61.8%), Extended (61.8%-78.6%), and Too Late (beyond 78.6%). The current price position within these zones determines whether a trading opportunity exists.

## The Entry Validation System

Having a pattern and knowing where you are in the retracement is only part of the equation. The indicator applies multiple filters before validating a trade signal:

**Pattern Strength Filter**: Only patterns scoring above 70% strength qualify for signals. This eliminates weak or ambiguous setups.

**Zone Filter**: Price must be in the Optimal or Acceptable zone. Trading extended or late zones dramatically reduces win probability.

**Risk-Reward Filter**: The calculated risk-reward ratio must exceed 2:1. This is configured via the `InpMinRR` parameter but defaults to a conservative 0.8 to allow some flexibility.

**Volatility Filter**: Excessive volatility (above 5% ATR relative to price) disqualifies trades to protect against unstable market conditions.

Here’s how the validation logic works:

```
void DetermineEntryValidity()  
{  
   m_structure.validForLong = false;  
   m_structure.validForShort = false;  
     
   if(m_structure.isBullish)  
   {  
      // All conditions must be true for valid long  
      m_structure.validForLong = m_structure.inOptimalZone &&   
                                  m_structure.rrRatio >= 2.0 &&  
                                  m_structure.patternStrength >= 70 &&  
                                  m_structure.volatility <= 5.0;  
   }  
}
```

This multi-factor approach mirrors how neural networks make decisions by weighing multiple inputs. A trade signal only generates when all conditions align, dramatically reducing false signals.

## Dynamic Stop Loss and Take Profit Calculation

The indicator doesn’t just tell you when to enter; it provides complete trade management levels calculated from the ATR (Average True Range):

```
void CalculateOptimalLevels()  
{  
   double currentPrice = iClose(m_symbol, m_timeframe, 0);  
     
   // Adjust ATR multipliers based on pattern strength  
   double atrMultiplierSL = 1.5;   // Default stop loss buffer  
   double atrMultiplierTP = 3.5;   // Default take profit target  
     
   // Stronger patterns allow tighter stops and wider targets  
   if(m_structure.patternStrength >= 90)  
   {  
      atrMultiplierSL = 1.2;  // Tighter stop for high-confidence trades  
      atrMultiplierTP = 4.5;  // More aggressive target  
   }  
     
   if(m_structure.isBullish)  
   {  
      // Stop loss below recent swing low with ATR buffer  
      m_structure.optimalSL = m_structure.lastLow - (m_structure.atr * atrMultiplierSL);  
        
      // Take profit above recent swing high with ATR extension  
      m_structure.optimalTP = m_structure.lastHigh + (m_structure.atr * atrMultiplierTP);  
   }  
}
```

This adaptive approach ensures your risk management adjusts to market conditions. High-confidence setups justify tighter stops and more aggressive targets, while weaker patterns require more conservative positioning.

## The Visual Interface: Real-Time Market Intelligence

The indicator’s panel provides at-a-glance market analysis updated every tick. This live feedback loop allows you to monitor pattern development without waiting for bar closes:

```
void UpdatePanel(string pattern, int strength, bool bullish, bool bearish,   
                 int signal, double support, double resistance,   
                 double price, double atr)  
{  
   // Pattern display with change notification  
   string patText = "Patrón: " + (pattern != "" ? pattern : "---");  
   if(pattern != g_lastPattern && g_lastPattern != "" && g_lastPattern != "RANGE")  
      patText += " 🆕";  // New pattern detected!  
     
   // Dynamic color coding based on direction  
   color patColor = bullish ? clrLime : bearish ? clrRed : clrGray;  
   ObjectSetString(0, g_panelPrefix + "Pattern", OBJPROP_TEXT, patText);  
   ObjectSetInteger(0, g_panelPrefix + "Pattern", OBJPROP_COLOR, patColor);  
}
```

The panel tracks pattern changes, strength evolution, and signal status in real-time. This immediate feedback helps you understand market dynamics as they unfold, rather than retrospectively analyzing closed bars.

## Signal Generation Logic: Precision Over Frequency

The indicator employs intelligent signal filtering to avoid spam. Signals only generate on new bar opens when specific conditions are met:

**Direction Change**: A shift from bullish to bearish structure or vice versa triggers evaluation.

**Pattern Change**: Transitioning between pattern types (for example, from HHL to HHH) indicates structural shift.

**Strength Increase**: A pattern gaining 15% or more in strength suggests momentum building.

**First Signal**: The initial pattern detection after a period of range behavior.

This creates a balance between staying responsive to market changes and avoiding excessive signal generation that can lead to overtrading.

## Practical Implementation Guide

To implement this indicator effectively, start with the M15 timeframe as specified in the default settings. This provides a sweet spot between signal frequency and reliability. The 15-minute chart offers enough data for meaningful pattern detection while generating actionable signals several times per trading session.

Configure your filters conservatively at first. Use the minimum strength setting of 70% to ensure you’re only trading the highest-probability setups. As you gain confidence with the system, you can experiment with lower thresholds for more signals, though this will reduce overall accuracy.

The panel position can be adjusted using the `InpPanelX` and `InpPanelY` parameters. Place it where it doesn't obscure important price action but remains easily visible during trading hours.

## Understanding the Visual Elements

The chart displays multiple visual components working together. Green arrows below candles indicate buy signals, while red arrows above indicate sells. The yellow dashed prediction line extends forward from signal bars, showing the anticipated price movement based on ATR.

Horizontal green and red lines mark dynamic support and resistance levels calculated from recent swing points. These aren’t static zones but adapt as new swings form. The white dotted line tracks current price for easy reference.

Signal labels appear directly on the chart at the moment of generation, showing the pattern name and strength percentage. This creates a visual history of market structure evolution.

## The Nobel Prize Connection

The 2024 Nobel Prize recognized how artificial neural networks can learn to recognize patterns in complex data. John Hopfield’s associative memory networks demonstrated how interconnected nodes could store and retrieve patterns, while Geoffrey Hinton’s backpropagation algorithm enabled networks to learn optimal feature representations.

This indicator applies these principles to financial markets. The pattern classification system acts like a neural network’s hidden layer, extracting meaningful features from raw price data. The strength scoring functions as a confidence metric similar to neural network output probabilities. The multi-factor validation process mirrors how deep networks combine multiple feature detectors to make robust predictions.

Just as neural networks transformed image recognition and natural language processing, these pattern recognition principles are revolutionizing technical analysis.

## Performance Considerations and Optimization

The indicator updates on every tick to maintain real-time panel information, but signal generation occurs only on new bar opens. This design balances responsiveness with computational efficiency. The debug output includes tick counting to monitor performance:

```
if(g_tickCount % 10 == 0 && !isNewBar)  
{  
   Print("⏱️ Tick #", g_tickCount, " | ", pattern, " | ",   
         strength, "% | Panel actualizado");  
}
```

For optimal performance, ensure your MetaTrader terminal has sufficient memory allocated. The indicator maintains minimal state (only the last 50 candles) to reduce memory footprint while providing comprehensive analysis.

## Advanced Customization Options

While the default parameters work well for most currency pairs, you can fine-tune several aspects. The `InpMinStrength` parameter controls signal sensitivity. Higher values (80-90) generate fewer but higher-quality signals. Lower values (30-50) increase signal frequency but reduce accuracy.

The `InpMinRR` parameter sets your minimum acceptable risk-reward ratio. Conservative traders might increase this to 1.5 or 2.0, while more aggressive approaches could lower it to 0.5. Remember that higher RR requirements mean fewer signals but better asymmetric risk profiles.

The `InpPredictionBars` parameter determines how far the yellow prediction line extends. Three bars provides a reasonable forward-looking window without excessive speculation.

## Conclusion: Bridging Physics and Finance

This indicator represents more than just another technical analysis tool. It embodies the fusion of cutting-edge pattern recognition principles with practical trading applications. By applying Nobel Prize-winning concepts to market analysis, we can identify high-probability setups with unprecedented precision.

The system’s strength lies in its comprehensive approach: pattern detection, zone analysis, risk management, and signal validation all work together as an integrated framework. Like a well-trained neural network, it processes multiple inputs to arrive at actionable decisions.

Whether you’re a novice trader seeking clear signals or an experienced analyst looking to systematize your approach, this indicator provides the structure and intelligence to navigate markets effectively.

## Complete Source Code

**Below you can add the complete code files:**

## PricePredictor\_Advanced\_v3.mqh

```
//+------------------------------------------------------------------+  
//| PricePredictor_Advanced_v2.mqh - ANÁLISIS AVANZADO HLC v7.0     |  
//| Detecta formación de velas y zonas óptimas de entrada           |  
//+------------------------------------------------------------------+  
#property copyright "Nobel Prize Physics 2024 - Advanced v7.0"  
#property version   "7.00"  
  
#define MAX_PATTERNS 50  
#define MAX_CANDLES 5  
  
//+------------------------------------------------------------------+  
enum ENUM_CANDLE_PATTERN  
{  
   PATTERN_NONE = 0,  
   PATTERN_HHH = 1,  
   PATTERN_HHL = 2,  
   PATTERN_HLH = 3,  
   PATTERN_HLL = 4,  
   PATTERN_LHH = 5,  
   PATTERN_LHL = 6,  
   PATTERN_LLH = 7,  
   PATTERN_LLL = 8,  
   PATTERN_RANGE = 9  
};  
  
//+------------------------------------------------------------------+  
enum ENUM_ENTRY_ZONE  
{  
   ZONE_NONE = 0,  
   ZONE_OPTIMAL = 1,  
   ZONE_ACCEPTABLE = 2,  
   ZONE_EXTENDED = 3,  
   ZONE_TOO_LATE = 4  
};  
  
//+------------------------------------------------------------------+  
struct CandleInfo  
{  
   double high;  
   double low;  
   double close;  
   double open;  
   datetime time;  
};  
  
//+------------------------------------------------------------------+  
struct MarketStructureAdvanced  
{  
   ENUM_CANDLE_PATTERN pattern;  
   string patternName;  
   int patternStrength;  
   bool isBullish;  
   bool isBearish;  
     
   double atr;  
   double volatility;  
     
   double lastHigh;  
   double lastLow;  
   double prevHigh;  
   double prevLow;  
   double prev2High;  
   double prev2Low;  
     
   double dynamicSupport;  
   double dynamicResistance;  
     
   double fib_382;  
   double fib_500;  
   double fib_618;  
   double fib_786;  
     
   ENUM_ENTRY_ZONE currentZone;  
   bool inOptimalZone;  
   double retracementPct;  
     
   double optimalEntry;  
   double optimalSL;  
   double optimalTP;  
     
   double rrRatio;  
   double confidence;  
   bool validForLong;  
   bool validForShort;  
     
   int consecutiveBullish;  
   int consecutiveBearish;  
};  
  
//+------------------------------------------------------------------+  
class CPricePredictorAdvanced  
{  
private:  
   string m_symbol;  
   ENUM_TIMEFRAMES m_timeframe;  
     
   MarketStructureAdvanced m_structure;  
   CandleInfo m_candles[MAX_CANDLES];  
   int m_candleCount;  
     
   double m_lastPrediction;  
   double m_lastConfidence;  
   double m_lastChange;  
   bool m_lastBullish;  
   datetime m_lastUpdate;  
     
   int m_atrPeriod;  
   int m_swingLookback;  
     
public:  
   CPricePredictorAdvanced(string symbol = NULL, ENUM_TIMEFRAMES tf = PERIOD_CURRENT)  
   {  
      m_symbol = (symbol == NULL) ? _Symbol : symbol;  
      m_timeframe = (tf == PERIOD_CURRENT) ? _Period : tf;  
        
      m_candleCount = 0;  
      m_lastPrediction = 0;  
      m_lastConfidence = 0;  
      m_lastChange = 0;  
      m_lastBullish = true;  
      m_lastUpdate = 0;  
        
      m_atrPeriod = 14;  
      m_swingLookback = 20;  
        
      ResetStructure();  
   }  
     
   void ResetStructure()  
   {  
      m_structure.pattern = PATTERN_NONE;  
      m_structure.patternName = "NONE";  
      m_structure.patternStrength = 0;  
      m_structure.isBullish = false;  
      m_structure.isBearish = false;  
      m_structure.atr = 0;  
      m_structure.volatility = 0;  
      m_structure.lastHigh = 0;  
      m_structure.lastLow = 0;  
      m_structure.prevHigh = 0;  
      m_structure.prevLow = 0;  
      m_structure.prev2High = 0;  
      m_structure.prev2Low = 0;  
      m_structure.dynamicSupport = 0;  
      m_structure.dynamicResistance = 0;  
      m_structure.fib_382 = 0;  
      m_structure.fib_500 = 0;  
      m_structure.fib_618 = 0;  
      m_structure.fib_786 = 0;  
      m_structure.currentZone = ZONE_NONE;  
      m_structure.inOptimalZone = false;  
      m_structure.retracementPct = 0;  
      m_structure.optimalEntry = 0;  
      m_structure.optimalSL = 0;  
      m_structure.optimalTP = 0;  
      m_structure.rrRatio = 0;  
      m_structure.confidence = 0;  
      m_structure.validForLong = false;  
      m_structure.validForShort = false;  
      m_structure.consecutiveBullish = 0;  
      m_structure.consecutiveBearish = 0;  
   }  
     
   bool Initialize()  
   {  
      Print("🚀 Predictor Advanced v7.0: ", m_symbol, " ", EnumToString(m_timeframe));  
        
      // Forzar primera actualización  
      UpdateAnalysis();  
        
      return true;  
   }  
     
   void UpdateAnalysis()  
   {  
      // RESETEAR estructura antes de cada análisis  
      ResetStructure();  
        
      LoadRecentCandles();  
      CalculateATR();  
      DetectSwingPoints();  
      AnalyzeCandlePattern();  
      CalculateFibonacciZones();  
      DetermineCurrentZone();  
      CalculateOptimalLevels();  
      DetermineEntryValidity();  
        
      m_lastUpdate = TimeCurrent();  
   }  
     
   void LoadRecentCandles()  
   {  
      m_candleCount = 0;  
        
      for(int i = 1; i <= MAX_CANDLES && m_candleCount < MAX_CANDLES; i++)  
      {  
         double high = iHigh(m_symbol, m_timeframe, i);  
         double low = iLow(m_symbol, m_timeframe, i);  
         double close = iClose(m_symbol, m_timeframe, i);  
         double open = iOpen(m_symbol, m_timeframe, i);  
         datetime time = iTime(m_symbol, m_timeframe, i);  
           
         // Validar datos  
         if(high > 0 && low > 0 && close > 0 && open > 0)  
         {  
            m_candles[m_candleCount].high = high;  
            m_candles[m_candleCount].low = low;  
            m_candles[m_candleCount].close = close;  
            m_candles[m_candleCount].open = open;  
            m_candles[m_candleCount].time = time;  
            m_candleCount++;  
         }  
      }  
   }  
     
   void CalculateATR()  
   {  
      double sum = 0;  
      int count = 0;  
        
      for(int i = 1; i <= m_atrPeriod; i++)  
      {  
         double high = iHigh(m_symbol, m_timeframe, i);  
         double low = iLow(m_symbol, m_timeframe, i);  
         double prevClose = iClose(m_symbol, m_timeframe, i + 1);  
           
         if(high > 0 && low > 0 && prevClose > 0)  
         {  
            double tr = MathMax(high - low, MathMax(  
                        MathAbs(high - prevClose),  
                        MathAbs(low - prevClose)));  
            sum += tr;  
            count++;  
         }  
      }  
        
      m_structure.atr = count > 0 ? sum / count : 0.0001;  
        
      double currentPrice = iClose(m_symbol, m_timeframe, 0);  
      m_structure.volatility = currentPrice > 0 ? (m_structure.atr / currentPrice) * 100.0 : 0;  
   }  
     
   void DetectSwingPoints()  
   {  
      int highCount = 0, lowCount = 0;  
        
      for(int i = 3; i < m_swingLookback && (highCount < 3 || lowCount < 3); i++)  
      {  
         // Detectar Swing Highs  
         if(highCount < 3)  
         {  
            bool isSwingHigh = true;  
            double highPrice = iHigh(m_symbol, m_timeframe, i);  
              
            if(highPrice > 0)  
            {  
               for(int j = 1; j <= 2; j++)  
               {  
                  double leftHigh = iHigh(m_symbol, m_timeframe, i - j);  
                  double rightHigh = iHigh(m_symbol, m_timeframe, i + j);  
                    
                  if(leftHigh >= highPrice || rightHigh >= highPrice)  
                  {  
                     isSwingHigh = false;  
                     break;  
                  }  
               }  
                 
               if(isSwingHigh)  
               {  
                  if(highCount == 0) m_structure.lastHigh = highPrice;  
                  else if(highCount == 1) m_structure.prevHigh = highPrice;  
                  else if(highCount == 2) m_structure.prev2High = highPrice;  
                  highCount++;  
               }  
            }  
         }  
           
         // Detectar Swing Lows  
         if(lowCount < 3)  
         {  
            bool isSwingLow = true;  
            double lowPrice = iLow(m_symbol, m_timeframe, i);  
              
            if(lowPrice > 0)  
            {  
               for(int j = 1; j <= 2; j++)  
               {  
                  double leftLow = iLow(m_symbol, m_timeframe, i - j);  
                  double rightLow = iLow(m_symbol, m_timeframe, i + j);  
                    
                  if(leftLow <= lowPrice || rightLow <= lowPrice)  
                  {  
                     isSwingLow = false;  
                     break;  
                  }  
               }  
                 
               if(isSwingLow)  
               {  
                  if(lowCount == 0) m_structure.lastLow = lowPrice;  
                  else if(lowCount == 1) m_structure.prevLow = lowPrice;  
                  else if(lowCount == 2) m_structure.prev2Low = lowPrice;  
                  lowCount++;  
               }  
            }  
         }  
      }  
        
      // Si no encontramos suficientes swings, usar datos de velas recientes  
      if(m_structure.lastHigh == 0 || m_structure.lastLow == 0)  
      {  
         double maxHigh = 0, maxHigh2 = 0;  
         double minLow = DBL_MAX, minLow2 = DBL_MAX;  
           
         for(int i = 1; i <= 10; i++)  
         {  
            double h = iHigh(m_symbol, m_timeframe, i);  
            double l = iLow(m_symbol, m_timeframe, i);  
              
            if(h > maxHigh) { maxHigh2 = maxHigh; maxHigh = h; }  
            else if(h > maxHigh2) maxHigh2 = h;  
              
            if(l < minLow) { minLow2 = minLow; minLow = l; }  
            else if(l < minLow2) minLow2 = l;  
         }  
           
         if(m_structure.lastHigh == 0) m_structure.lastHigh = maxHigh;  
         if(m_structure.prevHigh == 0) m_structure.prevHigh = maxHigh2;  
         if(m_structure.prev2High == 0) m_structure.prev2High = maxHigh2 * 0.999;  
           
         if(m_structure.lastLow == 0) m_structure.lastLow = minLow;  
         if(m_structure.prevLow == 0) m_structure.prevLow = minLow2;  
         if(m_structure.prev2Low == 0) m_structure.prev2Low = minLow2 * 1.001;  
      }  
   }  
     
   void AnalyzeCandlePattern()  
   {  
      // Resetear estado  
      m_structure.isBullish = false;  
      m_structure.isBearish = false;  
        
      if(m_structure.lastHigh == 0 || m_structure.prevHigh == 0 ||   
         m_structure.lastLow == 0 || m_structure.prevLow == 0)  
      {  
         m_structure.pattern = PATTERN_RANGE;  
         m_structure.patternName = "RANGE";  
         m_structure.patternStrength = 20;  
         return;  
      }  
        
      bool HH = m_structure.lastHigh > m_structure.prevHigh;  
      bool HL = m_structure.lastHigh < m_structure.prevHigh;  
      bool HiL = m_structure.lastLow > m_structure.prevLow;  
      bool LoL = m_structure.lastLow < m_structure.prevLow;  
        
      // Analizar patrones  
      if(HH && HiL)  
      {  
         if(m_structure.prevHigh > m_structure.prev2High &&   
            m_structure.prevLow > m_structure.prev2Low)  
         {  
            m_structure.pattern = PATTERN_HHH;  
            m_structure.patternName = "HHH";  
            m_structure.patternStrength = 95;  
            m_structure.isBullish = true;  
            m_structure.consecutiveBullish = 3;  
         }  
         else  
         {  
            m_structure.pattern = PATTERN_HHL;  
            m_structure.patternName = "HHL";  
            m_structure.patternStrength = 75;  
            m_structure.isBullish = true;  
            m_structure.consecutiveBullish = 2;  
         }  
      }  
      else if(HH && LoL)  
      {  
         m_structure.pattern = PATTERN_HLH;  
         m_structure.patternName = "HLH";  
         m_structure.patternStrength = 85;  
         m_structure.isBullish = true;  
         m_structure.consecutiveBullish = 2;  
      }  
      else if(HL && HiL)  
      {  
         m_structure.pattern = PATTERN_LHH;  
         m_structure.patternName = "LHH";  
         m_structure.patternStrength = 50;  
      }  
      else if(HL && LoL)  
      {  
         if(m_structure.prevHigh < m_structure.prev2High &&   
            m_structure.prevLow < m_structure.prev2Low)  
         {  
            m_structure.pattern = PATTERN_LLL;  
            m_structure.patternName = "LLL";  
            m_structure.patternStrength = 95;  
            m_structure.isBearish = true;  
            m_structure.consecutiveBearish = 3;  
         }  
         else  
         {  
            m_structure.pattern = PATTERN_LHL;  
            m_structure.patternName = "LHL";  
            m_structure.patternStrength = 85;  
            m_structure.isBearish = true;  
            m_structure.consecutiveBearish = 2;  
         }  
      }  
      else if(!HH && HiL)  
      {  
         m_structure.pattern = PATTERN_HLL;  
         m_structure.patternName = "HLL";  
         m_structure.patternStrength = 40;  
      }  
      else if(HL && !LoL)  
      {  
         m_structure.pattern = PATTERN_LLH;  
         m_structure.patternName = "LLH";  
         m_structure.patternStrength = 60;  
         m_structure.isBearish = true;  
         m_structure.consecutiveBearish = 1;  
      }  
      else  
      {  
         m_structure.pattern = PATTERN_RANGE;  
         m_structure.patternName = "RANGE";  
         m_structure.patternStrength = 20;  
      }  
        
      m_structure.confidence = m_structure.patternStrength;  
        
      if(m_structure.consecutiveBullish >= 2)  
         m_structure.confidence = MathMin(100, m_structure.confidence + 10);  
      if(m_structure.consecutiveBearish >= 2)  
         m_structure.confidence = MathMin(100, m_structure.confidence + 10);  
   }  
     
   void CalculateFibonacciZones()  
   {  
      m_structure.dynamicSupport = MathMin(m_structure.lastLow, m_structure.prevLow);  
      m_structure.dynamicResistance = MathMax(m_structure.lastHigh, m_structure.prevHigh);  
        
      double range = m_structure.dynamicResistance - m_structure.dynamicSupport;  
        
      if(range <= 0) range = m_structure.atr * 2;  
        
      if(m_structure.isBullish)  
      {  
         m_structure.fib_382 = m_structure.dynamicResistance - (range * 0.382);  
         m_structure.fib_500 = m_structure.dynamicResistance - (range * 0.500);  
         m_structure.fib_618 = m_structure.dynamicResistance - (range * 0.618);  
         m_structure.fib_786 = m_structure.dynamicResistance - (range * 0.786);  
      }  
      else if(m_structure.isBearish)  
      {  
         m_structure.fib_382 = m_structure.dynamicSupport + (range * 0.382);  
         m_structure.fib_500 = m_structure.dynamicSupport + (range * 0.500);  
         m_structure.fib_618 = m_structure.dynamicSupport + (range * 0.618);  
         m_structure.fib_786 = m_structure.dynamicSupport + (range * 0.786);  
      }  
      else  
      {  
         double mid = (m_structure.dynamicSupport + m_structure.dynamicResistance) / 2;  
         m_structure.fib_382 = mid;  
         m_structure.fib_500 = mid;  
         m_structure.fib_618 = mid;  
         m_structure.fib_786 = mid;  
      }  
   }  
     
   void DetermineCurrentZone()  
   {  
      double currentPrice = iClose(m_symbol, m_timeframe, 0);  
        
      m_structure.currentZone = ZONE_NONE;  
      m_structure.inOptimalZone = false;  
        
      if(m_structure.isBullish)  
      {  
         if(currentPrice >= m_structure.fib_382 && currentPrice <= m_structure.fib_500)  
         {  
            m_structure.currentZone = ZONE_OPTIMAL;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice >= m_structure.fib_500 && currentPrice <= m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_ACCEPTABLE;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice >= m_structure.fib_618 && currentPrice <= m_structure.fib_786)  
         {  
            m_structure.currentZone = ZONE_EXTENDED;  
         }  
         else if(currentPrice < m_structure.fib_786)  
         {  
            m_structure.currentZone = ZONE_TOO_LATE;  
         }  
           
         double range = m_structure.dynamicResistance - m_structure.dynamicSupport;  
         double retracement = m_structure.dynamicResistance - currentPrice;  
         m_structure.retracementPct = range > 0 ? (retracement / range) * 100.0 : 0;  
      }  
      else if(m_structure.isBearish)  
      {  
         if(currentPrice <= m_structure.fib_382 && currentPrice >= m_structure.fib_500)  
         {  
            m_structure.currentZone = ZONE_OPTIMAL;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice <= m_structure.fib_500 && currentPrice >= m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_ACCEPTABLE;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice <= m_structure.fib_618 && currentPrice >= m_structure.fib_786)  
         {  
            m_structure.currentZone = ZONE_EXTENDED;  
         }  
         else if(currentPrice > m_structure.fib_786)  
         {  
            m_structure.currentZone = ZONE_TOO_LATE;  
         }  
           
         double range = m_structure.dynamicResistance - m_structure.dynamicSupport;  
         double retracement = currentPrice - m_structure.dynamicSupport;  
         m_structure.retracementPct = range > 0 ? (retracement / range) * 100.0 : 0;  
      }  
   }  
     
   void CalculateOptimalLevels()  
   {  
      double currentPrice = iClose(m_symbol, m_timeframe, 0);  
        
      double atrMultiplierSL = 1.5;  
      double atrMultiplierTP = 3.5;  
        
      if(m_structure.patternStrength >= 90)  
      {  
         atrMultiplierSL = 1.2;  
         atrMultiplierTP = 4.5;  
      }  
      else if(m_structure.patternStrength <= 50)  
      {  
         atrMultiplierSL = 2.0;  
         atrMultiplierTP = 2.5;  
      }  
        
      if(m_structure.isBullish)  
      {  
         m_structure.optimalEntry = m_structure.inOptimalZone ? currentPrice : m_structure.fib_500;  
         m_structure.optimalSL = m_structure.lastLow - (m_structure.atr * atrMultiplierSL);  
         m_structure.optimalTP = m_structure.lastHigh + (m_structure.atr * atrMultiplierTP);  
           
         double risk = m_structure.optimalEntry - m_structure.optimalSL;  
         double reward = m_structure.optimalTP - m_structure.optimalEntry;  
         m_structure.rrRatio = risk > 0 ? reward / risk : 0;  
      }  
      else if(m_structure.isBearish)  
      {  
         m_structure.optimalEntry = m_structure.inOptimalZone ? currentPrice : m_structure.fib_500;  
         m_structure.optimalSL = m_structure.lastHigh + (m_structure.atr * atrMultiplierSL);  
         m_structure.optimalTP = m_structure.lastLow - (m_structure.atr * atrMultiplierTP);  
           
         double risk = m_structure.optimalSL - m_structure.optimalEntry;  
         double reward = m_structure.optimalEntry - m_structure.optimalTP;  
         m_structure.rrRatio = risk > 0 ? reward / risk : 0;  
      }  
      else  
      {  
         m_structure.optimalEntry = currentPrice;  
         m_structure.optimalSL = currentPrice;  
         m_structure.optimalTP = currentPrice;  
         m_structure.rrRatio = 0;  
      }  
   }  
     
   void DetermineEntryValidity()  
   {  
      m_structure.validForLong = false;  
      m_structure.validForShort = false;  
        
      if(m_structure.isBullish)  
      {  
         m_structure.validForLong = m_structure.inOptimalZone &&   
                                     m_structure.rrRatio >= 2.0 &&  
                                     m_structure.patternStrength >= 70 &&  
                                     m_structure.volatility <= 5.0;  
      }  
        
      if(m_structure.isBearish)  
      {  
         m_structure.validForShort = m_structure.inOptimalZone &&   
                                      m_structure.rrRatio >= 2.0 &&  
                                      m_structure.patternStrength >= 70 &&  
                                      m_structure.volatility <= 5.0;  
      }  
   }  
     
   // Getters  
   ENUM_CANDLE_PATTERN GetPattern() { return m_structure.pattern; }  
   string GetPatternName() { return m_structure.patternName; }  
   int GetPatternStrength() { return m_structure.patternStrength; }  
   bool IsBullish() { return m_structure.isBullish; }  
   bool IsBearish() { return m_structure.isBearish; }  
     
   double GetATR() { return m_structure.atr; }  
   double GetVolatility() { return m_structure.volatility; }  
     
   double GetSupport() { return m_structure.dynamicSupport; }  
   double GetResistance() { return m_structure.dynamicResistance; }  
   double GetOptimalEntry() { return m_structure.optimalEntry; }  
   double GetOptimalSL() { return m_structure.optimalSL; }  
   double GetOptimalTP() { return m_structure.optimalTP; }  
     
   double GetFib382() { return m_structure.fib_382; }  
   double GetFib500() { return m_structure.fib_500; }  
   double GetFib618() { return m_structure.fib_618; }  
   double GetFib786() { return m_structure.fib_786; }  
     
   int GetCurrentZone() { return (int)m_structure.currentZone; }  
   bool IsInOptimalZone() { return m_structure.inOptimalZone; }  
   double GetRetracementPct() { return m_structure.retracementPct; }  
   double GetRRRatio() { return m_structure.rrRatio; }  
     
   double GetConfidence() { return m_structure.confidence; }  
   bool IsValidForLong() { return m_structure.validForLong; }  
   bool IsValidForShort() { return m_structure.validForShort; }  
     
   int GetConsecutiveBullish() { return m_structure.consecutiveBullish; }  
   int GetConsecutiveBearish() { return m_structure.consecutiveBearish; }  
     
   ENUM_TIMEFRAMES GetTimeframe() { return m_timeframe; }  
};  
//+------------------------------------------------------------------+
```

## Nobel\_Simple\_Signals.mq5

```
//+------------------------------------------------------------------+  
//| Nobel_Simple_Signals.mq5 - INDICADOR SIMPLE Y EFECTIVO          |  
//| Muestra señales claras y predicciones visuales                  |  
//+------------------------------------------------------------------+  
#property copyright "Nobel Prize Physics 2024 - Simple v1.0"  
#property version   "1.00"  
#property indicator_chart_window  
#property indicator_buffers 6  
#property indicator_plots 6  
  
#include <PricePredictor_Advanced_v3.mqh>  
  
//--- Plots  
#property indicator_label1 "BUY"  
#property indicator_type1 DRAW_ARROW  
#property indicator_color1 clrLime  
#property indicator_width1 5  
  
#property indicator_label2 "SELL"  
#property indicator_type2 DRAW_ARROW  
#property indicator_color2 clrRed  
#property indicator_width2 5  
  
#property indicator_label3 "Predicción"  
#property indicator_type3 DRAW_LINE  
#property indicator_color3 clrYellow  
#property indicator_width3 3  
#property indicator_style3 STYLE_DASH  
  
#property indicator_label4 "Soporte"  
#property indicator_type4 DRAW_LINE  
#property indicator_color4 clrLime  
#property indicator_width4 2  
  
#property indicator_label5 "Resistencia"  
#property indicator_type5 DRAW_LINE  
#property indicator_color5 clrRed  
#property indicator_width5 2  
  
#property indicator_label6 "Precio Actual"  
#property indicator_type6 DRAW_LINE  
#property indicator_color6 clrWhite  
#property indicator_width6 1  
#property indicator_style6 STYLE_DOT  
  
//--- Inputs  
input group "=== CONFIGURACIÓN ==="  
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M15;  
input int InpPredictionBars = 3;  
input bool InpShowPanel = true;  
input int InpPanelX = 20;  
input int InpPanelY = 50;  
  
input group "=== FILTROS ==="  
input int InpMinStrength = 30;  
input double InpMinRR = 0.8;  
  
//--- Buffers  
double BuyBuffer[];  
double SellBuffer[];  
double PredictionBuffer[];  
double SupportBuffer[];  
double ResistanceBuffer[];  
double CurrentPriceBuffer[];  
  
//--- Globals  
CPricePredictorAdvanced* g_predictor = NULL;  
datetime g_lastBar = 0;  
datetime g_lastSignalBar = 0;  
string g_panelPrefix = "Panel_";  
int g_signalCount = 0;  
int g_tickCount = 0;  
  
// Cache de análisis anterior  
string g_lastPattern = "";  
int g_lastStrength = 0;  
bool g_lastBullish = false;  
bool g_lastBearish = false;  
  
//+------------------------------------------------------------------+  
int OnInit()  
{  
   //--- Setup buffers  
   SetIndexBuffer(0, BuyBuffer, INDICATOR_DATA);  
   SetIndexBuffer(1, SellBuffer, INDICATOR_DATA);  
   SetIndexBuffer(2, PredictionBuffer, INDICATOR_DATA);  
   SetIndexBuffer(3, SupportBuffer, INDICATOR_DATA);  
   SetIndexBuffer(4, ResistanceBuffer, INDICATOR_DATA);  
   SetIndexBuffer(5, CurrentPriceBuffer, INDICATOR_DATA);  
     
   //--- Arrows  
   PlotIndexSetInteger(0, PLOT_ARROW, 233);  
   PlotIndexSetInteger(1, PLOT_ARROW, 234);  
     
   //--- Shift prediction  
   PlotIndexSetInteger(2, PLOT_SHIFT, 1);  
     
   //--- Empty values  
   PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0);  
     
   //--- Initialize arrays  
   ArraySetAsSeries(BuyBuffer, true);  
   ArraySetAsSeries(SellBuffer, true);  
   ArraySetAsSeries(PredictionBuffer, true);  
   ArraySetAsSeries(SupportBuffer, true);  
   ArraySetAsSeries(ResistanceBuffer, true);  
   ArraySetAsSeries(CurrentPriceBuffer, true);  
     
   //--- Initialize predictor  
   g_predictor = new CPricePredictorAdvanced(_Symbol, InpTimeframe);  
   if(g_predictor == NULL || !g_predictor.Initialize())  
   {  
      Print("❌ ERROR: No se pudo inicializar");  
      return INIT_FAILED;  
   }  
     
   //--- Create panel  
   if(InpShowPanel)  
      CreatePanel();  
     
   Print("✅ Nobel Simple Signals iniciado");  
   Print("   Timeframe: ", EnumToString(InpTimeframe));  
     
   return INIT_SUCCEEDED;  
}  
  
//+------------------------------------------------------------------+  
void OnDeinit(const int reason)  
{  
   if(g_predictor != NULL)  
      delete g_predictor;  
     
   ObjectsDeleteAll(0, g_panelPrefix);  
   ObjectsDeleteAll(0, "Signal_");  
}  
  
//+------------------------------------------------------------------+  
bool CheckNewBar(datetime currentBarTime)  
{  
   if(currentBarTime != g_lastBar)  
   {  
      g_lastBar = currentBarTime;  
      return true;  
   }  
   return false;  
}  
  
//+------------------------------------------------------------------+  
int OnCalculate(const int rates_total,  
                const int prev_calculated,  
                const datetime &time[],  
                const double &open[],  
                const double &high[],  
                const double &low[],  
                const double &close[],  
                const long &tick_volume[],  
                const long &volume[],  
                const int &spread[])  
{  
   if(rates_total < 100) return 0;  
     
   // Set arrays as series  
   ArraySetAsSeries(time, true);  
   ArraySetAsSeries(open, true);  
   ArraySetAsSeries(high, true);  
   ArraySetAsSeries(low, true);  
   ArraySetAsSeries(close, true);  
     
   datetime currentBar = time[0];  
   bool isNewBar = CheckNewBar(currentBar);  
     
   g_tickCount++;  
     
   //--- SIEMPRE actualizar análisis en cada tick  
   g_predictor.UpdateAnalysis();  
     
   //--- Obtener datos frescos  
   string pattern = g_predictor.GetPatternName();  
   int strength = g_predictor.GetPatternStrength();  
   bool isBullish = g_predictor.IsBullish();  
   bool isBearish = g_predictor.IsBearish();  
   double atr = g_predictor.GetATR();  
   double support = g_predictor.GetSupport();  
   double resistance = g_predictor.GetResistance();  
   double rrRatio = g_predictor.GetRRRatio();  
     
   double currentPrice = close[0];  
     
   //--- Determinar señal potencial (sin generarla aún)  
   int currentSignal = 0;  
     
   // Lógica de señal más simple y directa  
   if(isBullish && strength >= InpMinStrength)  
   {  
      currentSignal = 1;  
   }  
   else if(isBearish && strength >= InpMinStrength)  
   {  
      currentSignal = -1;  
   }  
     
   //--- SIEMPRE actualizar panel (cada tick)  
   if(InpShowPanel)  
   {  
      UpdatePanel(pattern, strength, isBullish, isBearish, currentSignal,   
                  support, resistance, currentPrice, atr);  
   }  
     
   //--- Dibujar líneas de soporte/resistencia  
   int limit = MathMin(50, rates_total);  
   for(int i = 0; i < limit; i++)  
   {  
      SupportBuffer[i] = support;  
      ResistanceBuffer[i] = resistance;  
      CurrentPriceBuffer[i] = currentPrice;  
   }  
     
   //--- Solo generar señales visuales en barra NUEVA  
   if(isNewBar)  
   {  
      // Debug  
      Print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");  
      Print("📊 NUEVA BARRA: ", TimeToString(currentBar));  
      Print("   Patrón: ", pattern, " (ant: ", g_lastPattern, ")");  
      Print("   Fuerza: ", strength, "% (ant: ", g_lastStrength, "%)");  
      Print("   Alcista: ", isBullish);  
      Print("   Bajista: ", isBearish);  
      Print("   R:R: ", DoubleToString(rrRatio, 2));  
      Print("   Señal: ", currentSignal == 1 ? "BUY" : currentSignal == -1 ? "SELL" : "NINGUNA");  
        
      //--- Determinar si generar señal nueva  
      bool shouldSignal = false;  
        
      if(currentSignal != 0)  
      {  
         // Cambio de dirección  
         bool directionChange = (isBullish != g_lastBullish) || (isBearish != g_lastBearish);  
           
         // Cambio de patrón  
         bool patternChange = (pattern != g_lastPattern) && (pattern != "RANGE");  
           
         // Aumento significativo de fuerza  
         bool strengthIncrease = (strength > g_lastStrength + 15);  
           
         // Primera señal  
         bool firstSignal = (g_lastPattern == "" || g_lastPattern == "RANGE");  
           
         shouldSignal = directionChange || patternChange || strengthIncrease || firstSignal;  
           
         Print("   Cambio dirección: ", directionChange);  
         Print("   Cambio patrón: ", patternChange);  
         Print("   Aumento fuerza: ", strengthIncrease);  
         Print("   Primera señal: ", firstSignal);  
         Print("   → GENERAR: ", shouldSignal);  
      }  
        
      //--- Generar señal visual  
      if(shouldSignal && currentSignal == 1 && rrRatio >= InpMinRR)  
      {  
         BuyBuffer[0] = low[0] - (atr * 0.5);  
         g_signalCount++;  
           
         CreateLabel(time[0], low[0] - (atr * 0.5),   
                     "BUY " + pattern + " (" + IntegerToString(strength) + "%)", clrLime);  
           
         Alert("🔥 BUY ", pattern, " | ", strength, "% | ", _Symbol);  
         DrawPrediction(0, currentPrice, atr, true);  
           
         Print("✅ SEÑAL BUY GENERADA");  
      }  
      else if(shouldSignal && currentSignal == -1 && rrRatio >= InpMinRR)  
      {  
         SellBuffer[0] = high[0] + (atr * 0.5);  
         g_signalCount++;  
           
         CreateLabel(time[0], high[0] + (atr * 0.5),   
                     "SELL " + pattern + " (" + IntegerToString(strength) + "%)", clrRed);  
           
         Alert("🔥 SELL ", pattern, " | ", strength, "% | ", _Symbol);  
         DrawPrediction(0, currentPrice, atr, false);  
           
         Print("✅ SEÑAL SELL GENERADA");  
      }  
        
      //--- Actualizar cache SIEMPRE en nueva barra  
      g_lastPattern = pattern;  
      g_lastStrength = strength;  
      g_lastBullish = isBullish;  
      g_lastBearish = isBearish;  
        
      Print("   Cache actualizado");  
      Print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");  
   }  
     
   // Debug cada 10 ticks  
   if(g_tickCount % 10 == 0 && !isNewBar)  
   {  
      Print("⏱️ Tick #", g_tickCount, " | ", pattern, " | ", strength, "% | Panel actualizado");  
   }  
     
   return rates_total;  
}  
  
//+------------------------------------------------------------------+  
void DrawPrediction(int startIdx, double startPrice, double atr, bool bullish)  
{  
   double increment = bullish ? atr * 0.3 : -atr * 0.3;  
     
   for(int i = 0; i < InpPredictionBars; i++)  
   {  
      int idx = startIdx + i;  
      if(idx >= 0 && idx < ArraySize(PredictionBuffer))  
         PredictionBuffer[idx] = startPrice + (increment * (i + 1));  
   }  
}  
  
//+------------------------------------------------------------------+  
void CreateLabel(datetime time, double price, string text, color clr)  
{  
   string objName = "Signal_" + TimeToString(time);  
     
   if(ObjectFind(0, objName) >= 0)  
      ObjectDelete(0, objName);  
     
   ObjectCreate(0, objName, OBJ_TEXT, 0, time, price);  
   ObjectSetString(0, objName, OBJPROP_TEXT, text);  
   ObjectSetInteger(0, objName, OBJPROP_COLOR, clr);  
   ObjectSetInteger(0, objName, OBJPROP_FONTSIZE, 10);  
   ObjectSetInteger(0, objName, OBJPROP_ANCHOR, ANCHOR_CENTER);  
}  
  
//+------------------------------------------------------------------+  
void CreatePanel()  
{  
   int x = InpPanelX;  
   int y = InpPanelY;  
   int h = 18;  
     
   //--- Background  
   ObjectCreate(0, g_panelPrefix + "BG", OBJ_RECTANGLE_LABEL, 0, 0, 0);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_XDISTANCE, x - 5);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_YDISTANCE, y - 5);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_XSIZE, 300);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_YSIZE, 230);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BGCOLOR, C'20,20,20');  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BORDER_TYPE, BORDER_FLAT);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_COLOR, clrDarkGray);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_WIDTH, 1);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_CORNER, CORNER_LEFT_UPPER);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BACK, true);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_SELECTABLE, false);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_HIDDEN, true);  
     
   //--- Title  
   CreateText(g_panelPrefix + "Title", x, y, "🔮 NOBEL SIGNALS", clrYellow, 11, true);  
     
   y += h + 5;  
   CreateText(g_panelPrefix + "Pattern", x, y, "Patrón: Iniciando...", clrWhite, 9);  
     
   y += h;  
   CreateText(g_panelPrefix + "Strength", x, y, "Fuerza: 0%", clrGray, 9);  
     
   y += h;  
   CreateText(g_panelPrefix + "Direction", x, y, "Dirección: ---", clrCyan, 9, true);  
     
   y += h + 5;  
   CreateText(g_panelPrefix + "Signal", x, y, "Señal: Esperando...", clrGray, 10, true);  
     
   y += h + 5;  
   CreateText(g_panelPrefix + "Sep1", x, y, "━━━━━━━━━━━━━━━━━━━━━━━━━━", clrDarkGray, 8);  
     
   y += h;  
   CreateText(g_panelPrefix + "Price", x, y, "Precio: ---", clrWhite, 9);  
     
   y += h;  
   CreateText(g_panelPrefix + "Support", x, y, "Soporte: ---", clrLime, 9);  
     
   y += h;  
   CreateText(g_panelPrefix + "Resistance", x, y, "Resistencia: ---", clrRed, 9);  
     
   y += h + 5;  
   CreateText(g_panelPrefix + "Sep2", x, y, "━━━━━━━━━━━━━━━━━━━━━━━━━━", clrDarkGray, 8);  
     
   y += h;  
   CreateText(g_panelPrefix + "Signals", x, y, "Señales: 0", clrWhite, 9);  
     
   ChartRedraw();  
}  
  
//+------------------------------------------------------------------+  
void CreateText(string name, int x, int y, string text, color clr, int size = 9, bool bold = false)  
{  
   if(ObjectFind(0, name) >= 0)  
      ObjectDelete(0, name);  
        
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);  
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);  
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);  
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);  
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER);  
   ObjectSetString(0, name, OBJPROP_FONT, bold ? "Arial Bold" : "Arial");  
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);  
   ObjectSetString(0, name, OBJPROP_TEXT, text);  
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);  
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);  
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);  
}  
  
//+------------------------------------------------------------------+  
void UpdatePanel(string pattern, int strength, bool bullish, bool bearish,   
                 int signal, double support, double resistance,   
                 double price, double atr)  
{  
   if(!InpShowPanel) return;  
     
   //--- Pattern  
   string patText = "Patrón: " + (pattern != "" ? pattern : "---");  
   if(pattern != g_lastPattern && g_lastPattern != "" && g_lastPattern != "RANGE")  
      patText += " 🆕";  
     
   color patColor = bullish ? clrLime : bearish ? clrRed : clrGray;  
   ObjectSetString(0, g_panelPrefix + "Pattern", OBJPROP_TEXT, patText);  
   ObjectSetInteger(0, g_panelPrefix + "Pattern", OBJPROP_COLOR, patColor);  
     
   //--- Strength  
   color strengthColor = strength >= 70 ? clrLime :   
                         strength >= 50 ? clrYellow :   
                         strength >= 30 ? clrOrange : clrGray;  
     
   string strText = "Fuerza: " + IntegerToString(strength) + "%";  
   int diff = strength - g_lastStrength;  
   if(diff > 5) strText += " ↗";  
   else if(diff < -5) strText += " ↘";  
     
   ObjectSetString(0, g_panelPrefix + "Strength", OBJPROP_TEXT, strText);  
   ObjectSetInteger(0, g_panelPrefix + "Strength", OBJPROP_COLOR, strengthColor);  
     
   //--- Direction  
   string dirText = "Dirección: ";  
   color dirColor = clrGray;  
     
   if(bullish && !bearish)  
   {  
      dirText += "ALCISTA 📈";  
      dirColor = clrLime;  
   }  
   else if(bearish && !bullish)  
   {  
      dirText += "BAJISTA 📉";  
      dirColor = clrRed;  
   }  
   else if(bullish && bearish)  
   {  
      dirText += "CONFLICTO ⚠️";  
      dirColor = clrYellow;  
   }  
   else  
   {  
      dirText += "LATERAL ➡️";  
      dirColor = clrGray;  
   }  
     
   ObjectSetString(0, g_panelPrefix + "Direction", OBJPROP_TEXT, dirText);  
   ObjectSetInteger(0, g_panelPrefix + "Direction", OBJPROP_COLOR, dirColor);  
     
   //--- Signal  
   string sigText = "Señal: ";  
   color sigColor = clrGray;  
     
   if(signal == 1)  
   {  
      sigText += "🔥 COMPRAR";  
      sigColor = clrLime;  
   }  
   else if(signal == -1)  
   {  
      sigText += "🔥 VENDER";  
      sigColor = clrRed;  
   }  
   else if(bullish && strength >= 40)  
   {  
      sigText += "⏳ Esperando alcista";  
      sigColor = clrYellow;  
   }  
   else if(bearish && strength >= 40)  
   {  
      sigText += "⏳ Esperando bajista";  
      sigColor = clrOrange;  
   }  
   else  
   {  
      sigText += "❌ Sin señal";  
      sigColor = clrGray;  
   }  
     
   ObjectSetString(0, g_panelPrefix + "Signal", OBJPROP_TEXT, sigText);  
   ObjectSetInteger(0, g_panelPrefix + "Signal", OBJPROP_COLOR, sigColor);  
     
   //--- Levels  
   ObjectSetString(0, g_panelPrefix + "Price", OBJPROP_TEXT,   
                   "Precio: " + DoubleToString(price, _Digits));  
     
   ObjectSetString(0, g_panelPrefix + "Support", OBJPROP_TEXT,   
                   "Soporte: " + DoubleToString(support, _Digits));  
     
   ObjectSetString(0, g_panelPrefix + "Resistance", OBJPROP_TEXT,   
                   "Resistencia: " + DoubleToString(resistance, _Digits));  
     
   ObjectSetString(0, g_panelPrefix + "Signals", OBJPROP_TEXT,   
                   "Señales: " + IntegerToString(g_signalCount));  
     
   ChartRedraw();  
}  
//+------------------------------------------------------------------+
```

*This indicator is provided for educational purposes. Always test thoroughly on demo accounts before live trading. Past performance does not guarantee future results.*

## PricePredictor\_Advanced\_v3\_Optimized.mqh

```
//+------------------------------------------------------------------+  
//| PricePredictor_Advanced_v3_Optimized.mqh - VERSIÓN OPTIMIZADA  |  
//| Reducción drástica de uso de memoria y CPU                      |  
//+------------------------------------------------------------------+  
#property copyright "Nobel Prize Physics 2024 - Advanced v7.1 Optimized"  
#property version   "7.10"  
  
// Reducción de constantes para menor uso de memoria  
#define MAX_CANDLES 5        // Mantenido - mínimo necesario  
#define SWING_LOOKBACK 15    // Reducido de 20 a 15  
  
//+------------------------------------------------------------------+  
enum ENUM_CANDLE_PATTERN  
{  
   PATTERN_NONE = 0,  
   PATTERN_HHH = 1,  
   PATTERN_HHL = 2,  
   PATTERN_HLH = 3,  
   PATTERN_HLL = 4,  
   PATTERN_LHH = 5,  
   PATTERN_LHL = 6,  
   PATTERN_LLH = 7,  
   PATTERN_LLL = 8,  
   PATTERN_RANGE = 9  
};  
  
//+------------------------------------------------------------------+  
enum ENUM_ENTRY_ZONE  
{  
   ZONE_NONE = 0,  
   ZONE_OPTIMAL = 1,  
   ZONE_ACCEPTABLE = 2,  
   ZONE_EXTENDED = 3,  
   ZONE_TOO_LATE = 4  
};  
  
//+------------------------------------------------------------------+  
// Estructura simplificada - solo datos esenciales  
struct MarketStructureAdvanced  
{  
   ENUM_CANDLE_PATTERN pattern;  
   string patternName;  
   int patternStrength;  
   bool isBullish;  
   bool isBearish;  
     
   double atr;  
   double volatility;  
     
   // Niveles clave  
   double lastHigh;  
   double lastLow;  
   double prevHigh;  
   double prevLow;  
   double prev2High;  
   double prev2Low;  
     
   double dynamicSupport;  
   double dynamicResistance;  
     
   // Fibonacci (solo los más importantes)  
   double fib_500;  
   double fib_618;  
     
   ENUM_ENTRY_ZONE currentZone;  
   bool inOptimalZone;  
     
   double optimalEntry;  
   double optimalSL;  
   double optimalTP;  
   double rrRatio;  
     
   double confidence;  
   bool validForLong;  
   bool validForShort;  
     
   int consecutiveBullish;  
   int consecutiveBearish;  
};  
  
//+------------------------------------------------------------------+  
class CPricePredictorAdvanced  
{  
private:  
   string m_symbol;  
   ENUM_TIMEFRAMES m_timeframe;  
     
   MarketStructureAdvanced m_structure;  
     
   // Cache de precios - evita acceder a iHigh/iLow repetidamente  
   double m_priceCache[30];  // Reducido  
   bool m_cacheValid;  
   datetime m_cacheTime;  
     
   int m_atrPeriod;  
     
public:  
   CPricePredictorAdvanced(string symbol = NULL, ENUM_TIMEFRAMES tf = PERIOD_CURRENT)  
   {  
      m_symbol = (symbol == NULL) ? _Symbol : symbol;  
      m_timeframe = (tf == PERIOD_CURRENT) ? _Period : tf;  
        
      m_atrPeriod = 14;  
      m_cacheValid = false;  
      m_cacheTime = 0;  
        
      ResetStructure();  
   }  
     
   void ResetStructure()  
   {  
      m_structure.pattern = PATTERN_NONE;  
      m_structure.patternName = "NONE";  
      m_structure.patternStrength = 0;  
      m_structure.isBullish = false;  
      m_structure.isBearish = false;  
      m_structure.atr = 0;  
      m_structure.volatility = 0;  
      m_structure.lastHigh = 0;  
      m_structure.lastLow = 0;  
      m_structure.prevHigh = 0;  
      m_structure.prevLow = 0;  
      m_structure.prev2High = 0;  
      m_structure.prev2Low = 0;  
      m_structure.dynamicSupport = 0;  
      m_structure.dynamicResistance = 0;  
      m_structure.fib_500 = 0;  
      m_structure.fib_618 = 0;  
      m_structure.currentZone = ZONE_NONE;  
      m_structure.inOptimalZone = false;  
      m_structure.optimalEntry = 0;  
      m_structure.optimalSL = 0;  
      m_structure.optimalTP = 0;  
      m_structure.rrRatio = 0;  
      m_structure.confidence = 0;  
      m_structure.validForLong = false;  
      m_structure.validForShort = false;  
      m_structure.consecutiveBullish = 0;  
      m_structure.consecutiveBearish = 0;  
   }  
     
   bool Initialize()  
   {  
      UpdateAnalysis();  
      return true;  
   }  
     
   //+------------------------------------------------------------------+  
   // OPTIMIZACIÓN PRINCIPAL: Cache de precios para evitar múltiples llamadas a iHigh/iLow  
   //+------------------------------------------------------------------+  
   void LoadPriceCache()  
   {  
      datetime currentTime = iTime(m_symbol, m_timeframe, 0);  
        
      // Solo recargar si cambió la barra  
      if(m_cacheValid && m_cacheTime == currentTime)  
         return;  
        
      // Cargar solo los precios necesarios (30 barras en lugar de recorrer más)  
      for(int i = 0; i < 30; i++)  
      {  
         double h = iHigh(m_symbol, m_timeframe, i);  
         double l = iLow(m_symbol, m_timeframe, i);  
         m_priceCache[i] = (h + l) / 2.0;  // Precio medio como referencia  
      }  
        
      m_cacheValid = true;  
      m_cacheTime = currentTime;  
   }  
     
   void UpdateAnalysis()  
   {  
      ResetStructure();  
        
      // Cargar cache de precios primero  
      LoadPriceCache();  
        
      // Análisis en orden óptimo  
      CalculateATR();  
      DetectSwingPointsOptimized();  
      AnalyzeCandlePattern();  
      CalculateFibonacciZones();  
      DetermineCurrentZone();  
      CalculateOptimalLevels();  
      DetermineEntryValidity();  
   }  
     
   void CalculateATR()  
   {  
      // Usar CopyHigh/CopyLow/CopyClose es más eficiente que múltiples iHigh/iLow  
      double highs[], lows[], closes[];  
      ArraySetAsSeries(highs, true);  
      ArraySetAsSeries(lows, true);  
      ArraySetAsSeries(closes, true);  
        
      int copied = CopyHigh(m_symbol, m_timeframe, 0, m_atrPeriod + 2, highs);  
      if(copied <= 0) return;  
        
      CopyLow(m_symbol, m_timeframe, 0, m_atrPeriod + 2, lows);  
      CopyClose(m_symbol, m_timeframe, 0, m_atrPeriod + 2, closes);  
        
      double sum = 0;  
      for(int i = 1; i <= m_atrPeriod; i++)  
      {  
         double tr = MathMax(highs[i] - lows[i],   
                     MathMax(MathAbs(highs[i] - closes[i+1]),  
                             MathAbs(lows[i] - closes[i+1])));  
         sum += tr;  
      }  
        
      m_structure.atr = sum / m_atrPeriod;  
        
      double currentPrice = closes[0];  
      m_structure.volatility = currentPrice > 0 ? (m_structure.atr / currentPrice) * 100.0 : 0;  
        
      ArrayFree(highs);  
      ArrayFree(lows);  
      ArrayFree(closes);  
   }  
     
   //+------------------------------------------------------------------+  
   // VERSIÓN OPTIMIZADA: Detección de swing points más eficiente  
   //+------------------------------------------------------------------+  
   void DetectSwingPointsOptimized()  
   {  
      double highs[], lows[];  
      ArraySetAsSeries(highs, true);  
      ArraySetAsSeries(lows, true);  
        
      // Copiar datos de una vez  
      int bars = SWING_LOOKBACK;  
      CopyHigh(m_symbol, m_timeframe, 0, bars, highs);  
      CopyLow(m_symbol, m_timeframe, 0, bars, lows);  
        
      int highCount = 0, lowCount = 0;  
        
      // Búsqueda simplificada - menos iteraciones  
      for(int i = 2; i < bars - 2 && (highCount < 3 || lowCount < 3); i++)  
      {  
         // Swing High  
         if(highCount < 3 &&   
            highs[i] > highs[i-1] && highs[i] > highs[i-2] &&  
            highs[i] > highs[i+1] && highs[i] > highs[i+2])  
         {  
            if(highCount == 0) m_structure.lastHigh = highs[i];  
            else if(highCount == 1) m_structure.prevHigh = highs[i];  
            else if(highCount == 2) m_structure.prev2High = highs[i];  
            highCount++;  
         }  
           
         // Swing Low  
         if(lowCount < 3 &&   
            lows[i] < lows[i-1] && lows[i] < lows[i-2] &&  
            lows[i] < lows[i+1] && lows[i] < lows[i+2])  
         {  
            if(lowCount == 0) m_structure.lastLow = lows[i];  
            else if(lowCount == 1) m_structure.prevLow = lows[i];  
            else if(lowCount == 2) m_structure.prev2Low = lows[i];  
            lowCount++;  
         }  
      }  
        
      // Fallback simplificado  
      if(m_structure.lastHigh == 0)  
      {  
         m_structure.lastHigh = highs[ArrayMaximum(highs, 0, 10)];  
         m_structure.prevHigh = m_structure.lastHigh * 0.999;  
         m_structure.prev2High = m_structure.lastHigh * 0.998;  
      }  
        
      if(m_structure.lastLow == 0)  
      {  
         m_structure.lastLow = lows[ArrayMinimum(lows, 0, 10)];  
         m_structure.prevLow = m_structure.lastLow * 1.001;  
         m_structure.prev2Low = m_structure.lastLow * 1.002;  
      }  
        
      ArrayFree(highs);  
      ArrayFree(lows);  
   }  
     
   void AnalyzeCandlePattern()  
   {  
      m_structure.isBullish = false;  
      m_structure.isBearish = false;  
        
      if(m_structure.lastHigh == 0 || m_structure.lastLow == 0)  
      {  
         m_structure.pattern = PATTERN_RANGE;  
         m_structure.patternName = "RANGE";  
         m_structure.patternStrength = 20;  
         return;  
      }  
        
      bool HH = m_structure.lastHigh > m_structure.prevHigh;  
      bool HL = m_structure.lastHigh < m_structure.prevHigh;  
      bool HiL = m_structure.lastLow > m_structure.prevLow;  
      bool LoL = m_structure.lastLow < m_structure.prevLow;  
        
      // Patrones simplificados  
      if(HH && HiL)  
      {  
         bool tripleHigh = m_structure.prevHigh > m_structure.prev2High &&   
                           m_structure.prevLow > m_structure.prev2Low;  
           
         m_structure.pattern = tripleHigh ? PATTERN_HHH : PATTERN_HHL;  
         m_structure.patternName = tripleHigh ? "HHH" : "HHL";  
         m_structure.patternStrength = tripleHigh ? 95 : 75;  
         m_structure.isBullish = true;  
         m_structure.consecutiveBullish = tripleHigh ? 3 : 2;  
      }  
      else if(HH && LoL)  
      {  
         m_structure.pattern = PATTERN_HLH;  
         m_structure.patternName = "HLH";  
         m_structure.patternStrength = 85;  
         m_structure.isBullish = true;  
         m_structure.consecutiveBullish = 2;  
      }  
      else if(HL && LoL)  
      {  
         bool tripleLow = m_structure.prevHigh < m_structure.prev2High &&   
                          m_structure.prevLow < m_structure.prev2Low;  
           
         m_structure.pattern = tripleLow ? PATTERN_LLL : PATTERN_LHL;  
         m_structure.patternName = tripleLow ? "LLL" : "LHL";  
         m_structure.patternStrength = tripleLow ? 95 : 85;  
         m_structure.isBearish = true;  
         m_structure.consecutiveBearish = tripleLow ? 3 : 2;  
      }  
      else if(HL && HiL)  
      {  
         m_structure.pattern = PATTERN_LHH;  
         m_structure.patternName = "LHH";  
         m_structure.patternStrength = 50;  
      }  
      else  
      {  
         m_structure.pattern = PATTERN_RANGE;  
         m_structure.patternName = "RANGE";  
         m_structure.patternStrength = 20;  
      }  
        
      m_structure.confidence = m_structure.patternStrength;  
   }  
     
   void CalculateFibonacciZones()  
   {  
      m_structure.dynamicSupport = MathMin(m_structure.lastLow, m_structure.prevLow);  
      m_structure.dynamicResistance = MathMax(m_structure.lastHigh, m_structure.prevHigh);  
        
      double range = m_structure.dynamicResistance - m_structure.dynamicSupport;  
      if(range <= 0) range = m_structure.atr * 2;  
        
      // Solo calcular Fib 50% y 61.8% (los más importantes)  
      if(m_structure.isBullish)  
      {  
         m_structure.fib_500 = m_structure.dynamicResistance - (range * 0.500);  
         m_structure.fib_618 = m_structure.dynamicResistance - (range * 0.618);  
      }  
      else if(m_structure.isBearish)  
      {  
         m_structure.fib_500 = m_structure.dynamicSupport + (range * 0.500);  
         m_structure.fib_618 = m_structure.dynamicSupport + (range * 0.618);  
      }  
      else  
      {  
         double mid = (m_structure.dynamicSupport + m_structure.dynamicResistance) / 2;  
         m_structure.fib_500 = mid;  
         m_structure.fib_618 = mid;  
      }  
   }  
     
   void DetermineCurrentZone()  
   {  
      double currentPrice = iClose(m_symbol, m_timeframe, 0);  
        
      m_structure.currentZone = ZONE_NONE;  
      m_structure.inOptimalZone = false;  
        
      if(m_structure.isBullish)  
      {  
         if(currentPrice >= m_structure.fib_500 && currentPrice <= m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_OPTIMAL;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice > m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_ACCEPTABLE;  
            m_structure.inOptimalZone = true;  
         }  
      }  
      else if(m_structure.isBearish)  
      {  
         if(currentPrice <= m_structure.fib_500 && currentPrice >= m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_OPTIMAL;  
            m_structure.inOptimalZone = true;  
         }  
         else if(currentPrice < m_structure.fib_618)  
         {  
            m_structure.currentZone = ZONE_ACCEPTABLE;  
            m_structure.inOptimalZone = true;  
         }  
      }  
   }  
     
   void CalculateOptimalLevels()  
   {  
      double currentPrice = iClose(m_symbol, m_timeframe, 0);  
        
      double atrMult = m_structure.patternStrength >= 90 ? 1.2 :   
                       m_structure.patternStrength <= 50 ? 2.0 : 1.5;  
        
      if(m_structure.isBullish)  
      {  
         m_structure.optimalEntry = m_structure.inOptimalZone ? currentPrice : m_structure.fib_500;  
         m_structure.optimalSL = m_structure.lastLow - (m_structure.atr * atrMult);  
         m_structure.optimalTP = m_structure.lastHigh + (m_structure.atr * 3.5);  
           
         double risk = m_structure.optimalEntry - m_structure.optimalSL;  
         double reward = m_structure.optimalTP - m_structure.optimalEntry;  
         m_structure.rrRatio = risk > 0 ? reward / risk : 0;  
      }  
      else if(m_structure.isBearish)  
      {  
         m_structure.optimalEntry = m_structure.inOptimalZone ? currentPrice : m_structure.fib_500;  
         m_structure.optimalSL = m_structure.lastHigh + (m_structure.atr * atrMult);  
         m_structure.optimalTP = m_structure.lastLow - (m_structure.atr * 3.5);  
           
         double risk = m_structure.optimalSL - m_structure.optimalEntry;  
         double reward = m_structure.optimalEntry - m_structure.optimalTP;  
         m_structure.rrRatio = risk > 0 ? reward / risk : 0;  
      }  
   }  
     
   void DetermineEntryValidity()  
   {  
      m_structure.validForLong = m_structure.isBullish &&   
                                  m_structure.inOptimalZone &&   
                                  m_structure.rrRatio >= 2.0 &&  
                                  m_structure.patternStrength >= 70;  
        
      m_structure.validForShort = m_structure.isBearish &&   
                                   m_structure.inOptimalZone &&   
                                   m_structure.rrRatio >= 2.0 &&  
                                   m_structure.patternStrength >= 70;  
   }  
     
   // Getters - sin cambios  
   ENUM_CANDLE_PATTERN GetPattern() { return m_structure.pattern; }  
   string GetPatternName() { return m_structure.patternName; }  
   int GetPatternStrength() { return m_structure.patternStrength; }  
   bool IsBullish() { return m_structure.isBullish; }  
   bool IsBearish() { return m_structure.isBearish; }  
     
   double GetATR() { return m_structure.atr; }  
   double GetVolatility() { return m_structure.volatility; }  
     
   double GetSupport() { return m_structure.dynamicSupport; }  
   double GetResistance() { return m_structure.dynamicResistance; }  
   double GetOptimalEntry() { return m_structure.optimalEntry; }  
   double GetOptimalSL() { return m_structure.optimalSL; }  
   double GetOptimalTP() { return m_structure.optimalTP; }  
     
   double GetFib500() { return m_structure.fib_500; }  
   double GetFib618() { return m_structure.fib_618; }  
     
   int GetCurrentZone() { return (int)m_structure.currentZone; }  
   bool IsInOptimalZone() { return m_structure.inOptimalZone; }  
   double GetRRRatio() { return m_structure.rrRatio; }  
     
   double GetConfidence() { return m_structure.confidence; }  
   bool IsValidForLong() { return m_structure.validForLong; }  
   bool IsValidForShort() { return m_structure.validForShort; }  
     
   int GetConsecutiveBullish() { return m_structure.consecutiveBullish; }  
   int GetConsecutiveBearish() { return m_structure.consecutiveBearish; }  
     
   ENUM_TIMEFRAMES GetTimeframe() { return m_timeframe; }  
};  
//+------------------------------------------------------------------+
```

## Nobel\_Simple\_Signals\_Optimized.mq5

```
//+------------------------------------------------------------------+  
//| Nobel_Simple_Signals_Optimized.mq5 - VERSIÓN OPTIMIZADA         |  
//| Reducción de uso de memoria y CPU                               |  
//+------------------------------------------------------------------+  
#property copyright "Nobel Prize Physics 2024 - Simple v1.1 Optimized"  
#property version   "1.10"  
#property indicator_chart_window  
#property indicator_buffers 6  
#property indicator_plots 6  
  
#include <PricePredictor_Advanced_v3_Optimized.mqh>  
  
//--- Plots (sin cambios)  
#property indicator_label1 "BUY"  
#property indicator_type1 DRAW_ARROW  
#property indicator_color1 clrLime  
#property indicator_width1 5  
  
#property indicator_label2 "SELL"  
#property indicator_type2 DRAW_ARROW  
#property indicator_color2 clrRed  
#property indicator_width2 5  
  
#property indicator_label3 "Predicción"  
#property indicator_type3 DRAW_LINE  
#property indicator_color3 clrYellow  
#property indicator_width3 3  
#property indicator_style3 STYLE_DASH  
  
#property indicator_label4 "Soporte"  
#property indicator_type4 DRAW_LINE  
#property indicator_color4 clrLime  
#property indicator_width4 2  
  
#property indicator_label5 "Resistencia"  
#property indicator_type5 DRAW_LINE  
#property indicator_color5 clrRed  
#property indicator_width5 2  
  
#property indicator_label6 "Precio Actual"  
#property indicator_type6 DRAW_LINE  
#property indicator_color6 clrWhite  
#property indicator_width6 1  
#property indicator_style6 STYLE_DOT  
  
//--- Inputs  
input group "=== CONFIGURACIÓN ==="  
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M15;  
input int InpPredictionBars = 3;  
input bool InpShowPanel = true;  
input int InpPanelX = 20;  
input int InpPanelY = 50;  
  
input group "=== FILTROS ==="  
input int InpMinStrength = 30;  
input double InpMinRR = 0.8;  
  
input group "=== OPTIMIZACIÓN ==="  
input int InpUpdateEveryNTicks = 5; // Actualizar panel cada N ticks (menos CPU)  
  
//--- Buffers  
double BuyBuffer[];  
double SellBuffer[];  
double PredictionBuffer[];  
double SupportBuffer[];  
double ResistanceBuffer[];  
double CurrentPriceBuffer[];  
  
//--- Globals  
CPricePredictorAdvanced* g_predictor = NULL;  
datetime g_lastBar = 0;  
string g_panelPrefix = "Panel_";  
int g_signalCount = 0;  
int g_tickCount = 0;  
  
// Cache simplificado - solo lo esencial  
string g_lastPattern = "";  
int g_lastStrength = 0;  
bool g_lastBullish = false;  
bool g_lastBearish = false;  
  
//+------------------------------------------------------------------+  
int OnInit()  
{  
   //--- Setup buffers  
   SetIndexBuffer(0, BuyBuffer, INDICATOR_DATA);  
   SetIndexBuffer(1, SellBuffer, INDICATOR_DATA);  
   SetIndexBuffer(2, PredictionBuffer, INDICATOR_DATA);  
   SetIndexBuffer(3, SupportBuffer, INDICATOR_DATA);  
   SetIndexBuffer(4, ResistanceBuffer, INDICATOR_DATA);  
   SetIndexBuffer(5, CurrentPriceBuffer, INDICATOR_DATA);  
     
   //--- Arrows  
   PlotIndexSetInteger(0, PLOT_ARROW, 233);  
   PlotIndexSetInteger(1, PLOT_ARROW, 234);  
     
   //--- Shift prediction  
   PlotIndexSetInteger(2, PLOT_SHIFT, 1);  
     
   //--- Empty values  
   PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0);  
   PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0);  
     
   //--- Initialize arrays as series  
   ArraySetAsSeries(BuyBuffer, true);  
   ArraySetAsSeries(SellBuffer, true);  
   ArraySetAsSeries(PredictionBuffer, true);  
   ArraySetAsSeries(SupportBuffer, true);  
   ArraySetAsSeries(ResistanceBuffer, true);  
   ArraySetAsSeries(CurrentPriceBuffer, true);  
     
   //--- Initialize predictor  
   g_predictor = new CPricePredictorAdvanced(_Symbol, InpTimeframe);  
   if(g_predictor == NULL || !g_predictor.Initialize())  
   {  
      Print("❌ ERROR: No se pudo inicializar");  
      return INIT_FAILED;  
   }  
     
   //--- Create panel  
   if(InpShowPanel)  
      CreatePanel();  
     
   Print("✅ Nobel Simple Signals Optimized iniciado");  
   Print("   Actualización panel: cada ", InpUpdateEveryNTicks, " ticks");  
     
   return INIT_SUCCEEDED;  
}  
  
//+------------------------------------------------------------------+  
void OnDeinit(const int reason)  
{  
   if(g_predictor != NULL)  
      delete g_predictor;  
     
   ObjectsDeleteAll(0, g_panelPrefix);  
   ObjectsDeleteAll(0, "Signal_");  
}  
  
//+------------------------------------------------------------------+  
int OnCalculate(const int rates_total,  
                const int prev_calculated,  
                const datetime &time[],  
                const double &open[],  
                const double &high[],  
                const double &low[],  
                const double &close[],  
                const long &tick_volume[],  
                const long &volume[],  
                const int &spread[])  
{  
   if(rates_total < 100) return 0;  
     
   // Set arrays as series  
   ArraySetAsSeries(time, true);  
   ArraySetAsSeries(close, true);  
   ArraySetAsSeries(high, true);  
   ArraySetAsSeries(low, true);  
     
   datetime currentBar = time[0];  
   bool isNewBar = (currentBar != g_lastBar);  
     
   if(isNewBar)  
      g_lastBar = currentBar;  
     
   g_tickCount++;  
     
   //--- OPTIMIZACIÓN: Solo actualizar análisis completo en NUEVA BARRA  
   //    Esto reduce drásticamente el consumo de CPU  
   if(isNewBar)  
   {  
      g_predictor.UpdateAnalysis();  
        
      //--- Obtener datos actualizados  
      string pattern = g_predictor.GetPatternName();  
      int strength = g_predictor.GetPatternStrength();  
      bool isBullish = g_predictor.IsBullish();  
      bool isBearish = g_predictor.IsBearish();  
      double atr = g_predictor.GetATR();  
      double support = g_predictor.GetSupport();  
      double resistance = g_predictor.GetResistance();  
      double rrRatio = g_predictor.GetRRRatio();  
        
      double currentPrice = close[0];  
        
      //--- Dibujar líneas de soporte/resistencia (solo primeras 50 barras)  
      int limit = MathMin(50, rates_total);  
      for(int i = 0; i < limit; i++)  
      {  
         SupportBuffer[i] = support;  
         ResistanceBuffer[i] = resistance;  
         CurrentPriceBuffer[i] = currentPrice;  
      }  
        
      //--- Determinar señal  
      int currentSignal = 0;  
        
      if(isBullish && strength >= InpMinStrength)  
         currentSignal = 1;  
      else if(isBearish && strength >= InpMinStrength)  
         currentSignal = -1;  
        
      //--- Verificar si debe generar señal visual  
      bool shouldSignal = false;  
        
      if(currentSignal != 0)  
      {  
         bool directionChange = (isBullish != g_lastBullish) || (isBearish != g_lastBearish);  
         bool patternChange = (pattern != g_lastPattern) && (pattern != "RANGE");  
         bool strengthIncrease = (strength > g_lastStrength + 15);  
         bool firstSignal = (g_lastPattern == "" || g_lastPattern == "RANGE");  
           
         shouldSignal = directionChange || patternChange || strengthIncrease || firstSignal;  
      }  
        
      //--- Generar señal visual  
      if(shouldSignal && currentSignal == 1 && rrRatio >= InpMinRR)  
      {  
         BuyBuffer[0] = low[0] - (atr * 0.5);  
         g_signalCount++;  
           
         CreateLabel(time[0], low[0] - (atr * 0.5),   
                     "BUY " + pattern + " (" + IntegerToString(strength) + "%)", clrLime);  
           
         Alert("🔥 BUY ", pattern, " | ", strength, "% | ", _Symbol);  
         DrawPrediction(0, currentPrice, atr, true);  
           
         Print("✅ BUY: ", pattern, " | Fuerza: ", strength, "% | R:R: ", DoubleToString(rrRatio, 2));  
      }  
      else if(shouldSignal && currentSignal == -1 && rrRatio >= InpMinRR)  
      {  
         SellBuffer[0] = high[0] + (atr * 0.5);  
         g_signalCount++;  
           
         CreateLabel(time[0], high[0] + (atr * 0.5),   
                     "SELL " + pattern + " (" + IntegerToString(strength) + "%)", clrRed);  
           
         Alert("🔥 SELL ", pattern, " | ", strength, "% | ", _Symbol);  
         DrawPrediction(0, currentPrice, atr, false);  
           
         Print("✅ SELL: ", pattern, " | Fuerza: ", strength, "% | R:R: ", DoubleToString(rrRatio, 2));  
      }  
        
      //--- Actualizar cache  
      g_lastPattern = pattern;  
      g_lastStrength = strength;  
      g_lastBullish = isBullish;  
      g_lastBearish = isBearish;  
        
      //--- Actualizar panel en nueva barra  
      if(InpShowPanel)  
      {  
         UpdatePanel(pattern, strength, isBullish, isBearish, currentSignal,   
                     support, resistance, currentPrice, atr);  
      }  
   }  
   else  
   {  
      //--- OPTIMIZACIÓN: En ticks intermedios, solo actualizar panel ocasionalmente  
      //    Esto evita redibujar el panel cientos de veces por segundo  
      if(InpShowPanel && g_tickCount % InpUpdateEveryNTicks == 0)  
      {  
         // Obtener solo datos ligeros sin recalcular todo  
         double currentPrice = close[0];  
         double support = g_predictor.GetSupport();  
         double resistance = g_predictor.GetResistance();  
         double atr = g_predictor.GetATR();  
           
         // Actualizar solo precio actual en el panel  
         UpdatePanelPriceOnly(currentPrice);  
      }  
   }  
     
   return rates_total;  
}  
  
//+------------------------------------------------------------------+  
void DrawPrediction(int startIdx, double startPrice, double atr, bool bullish)  
{  
   double increment = bullish ? atr * 0.3 : -atr * 0.3;  
     
   for(int i = 0; i < InpPredictionBars; i++)  
   {  
      int idx = startIdx + i;  
      if(idx >= 0 && idx < ArraySize(PredictionBuffer))  
         PredictionBuffer[idx] = startPrice + (increment * (i + 1));  
   }  
}  
  
//+------------------------------------------------------------------+  
void CreateLabel(datetime time, double price, string text, color clr)  
{  
   string objName = "Signal_" + TimeToString(time);  
     
   if(ObjectFind(0, objName) >= 0)  
      ObjectDelete(0, objName);  
     
   ObjectCreate(0, objName, OBJ_TEXT, 0, time, price);  
   ObjectSetString(0, objName, OBJPROP_TEXT, text);  
   ObjectSetInteger(0, objName, OBJPROP_COLOR, clr);  
   ObjectSetInteger(0, objName, OBJPROP_FONTSIZE, 10);  
   ObjectSetInteger(0, objName, OBJPROP_ANCHOR, ANCHOR_CENTER);  
}  
  
//+------------------------------------------------------------------+  
void CreatePanel()  
{  
   int x = InpPanelX;  
   int y = InpPanelY;  
   int h = 18;  
     
   ObjectCreate(0, g_panelPrefix + "BG", OBJ_RECTANGLE_LABEL, 0, 0, 0);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_XDISTANCE, x - 5);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_YDISTANCE, y - 5);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_XSIZE, 300);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_YSIZE, 230);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BGCOLOR, C'20,20,20');  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BORDER_TYPE, BORDER_FLAT);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_COLOR, clrDarkGray);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_CORNER, CORNER_LEFT_UPPER);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_BACK, true);  
   ObjectSetInteger(0, g_panelPrefix + "BG", OBJPROP_SELECTABLE, false);  
     
   CreateText(g_panelPrefix + "Title", x, y, "🔮 NOBEL SIGNALS", clrYellow, 11, true);  
   y += h + 5;  
   CreateText(g_panelPrefix + "Pattern", x, y, "Patrón: Iniciando...", clrWhite, 9);  
   y += h;  
   CreateText(g_panelPrefix + "Strength", x, y, "Fuerza: 0%", clrGray, 9);  
   y += h;  
   CreateText(g_panelPrefix + "Direction", x, y, "Dirección: ---", clrCyan, 9, true);  
   y += h + 5;  
   CreateText(g_panelPrefix + "Signal", x, y, "Señal: Esperando...", clrGray, 10, true);  
   y += h + 5;  
   CreateText(g_panelPrefix + "Sep1", x, y, "━━━━━━━━━━━━━━━━━━━━━━━━━━", clrDarkGray, 8);  
   y += h;  
   CreateText(g_panelPrefix + "Price", x, y, "Precio: ---", clrWhite, 9);  
   y += h;  
   CreateText(g_panelPrefix + "Support", x, y, "Soporte: ---", clrLime, 9);  
   y += h;  
   CreateText(g_panelPrefix + "Resistance", x, y, "Resistencia: ---", clrRed, 9);  
   y += h + 5;  
   CreateText(g_panelPrefix + "Sep2", x, y, "━━━━━━━━━━━━━━━━━━━━━━━━━━", clrDarkGray, 8);  
   y += h;  
   CreateText(g_panelPrefix + "Signals", x, y, "Señales: 0", clrWhite, 9);  
     
   ChartRedraw();  
}  
  
//+------------------------------------------------------------------+  
void CreateText(string name, int x, int y, string text, color clr, int size = 9, bool bold = false)  
{  
   if(ObjectFind(0, name) >= 0)  
      ObjectDelete(0, name);  
        
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);  
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);  
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);  
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);  
   ObjectSetString(0, name, OBJPROP_FONT, bold ? "Arial Bold" : "Arial");  
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);  
   ObjectSetString(0, name, OBJPROP_TEXT, text);  
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);  
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);  
}  
  
//+------------------------------------------------------------------+  
// NUEVA FUNCIÓN: Actualización ligera solo del precio  
void UpdatePanelPriceOnly(double price)  
{  
   ObjectSetString(0, g_panelPrefix + "Price", OBJPROP_TEXT,   
                   "Precio: " + DoubleToString(price, _Digits));  
}  
  
//+------------------------------------------------------------------+  
void UpdatePanel(string pattern, int strength, bool bullish, bool bearish,   
                 int signal, double support, double resistance,   
                 double price, double atr)  
{  
   if(!InpShowPanel) return;  
     
   //--- Pattern  
   string patText = "Patrón: " + (pattern != "" ? pattern : "---");  
   color patColor = bullish ? clrLime : bearish ? clrRed : clrGray;  
   ObjectSetString(0, g_panelPrefix + "Pattern", OBJPROP_TEXT, patText);  
   ObjectSetInteger(0, g_panelPrefix + "Pattern", OBJPROP_COLOR, patColor);  
     
   //--- Strength  
   color strengthColor = strength >= 70 ? clrLime :   
                         strength >= 50 ? clrYellow :   
                         strength >= 30 ? clrOrange : clrGray;  
     
   ObjectSetString(0, g_panelPrefix + "Strength", OBJPROP_TEXT,   
                   "Fuerza: " + IntegerToString(strength) + "%");  
   ObjectSetInteger(0, g_panelPrefix + "Strength", OBJPROP_COLOR, strengthColor);  
     
   //--- Direction  
   string dirText = "Dirección: ";  
   color dirColor = clrGray;  
     
   if(bullish && !bearish)  
   {  
      dirText += "ALCISTA 📈";  
      dirColor = clrLime;  
   }  
   else if(bearish && !bullish)  
   {  
      dirText += "BAJISTA 📉";  
      dirColor = clrRed;  
   }  
   else if(bullish && bearish)  
   {  
      dirText += "CONFLICTO ⚠️";  
      dirColor = clrYellow;  
   }  
   else  
   {  
      dirText += "LATERAL ➡️";  
      dirColor = clrGray;  
   }  
     
   ObjectSetString(0, g_panelPrefix + "Direction", OBJPROP_TEXT, dirText);  
   ObjectSetInteger(0, g_panelPrefix + "Direction", OBJPROP_COLOR, dirColor);  
     
   //--- Signal  
   string sigText = "Señal: ";  
   color sigColor = clrGray;  
     
   if(signal == 1)  
   {  
      sigText += "🔥 COMPRAR";  
      sigColor = clrLime;  
   }  
   else if(signal == -1)  
   {  
      sigText += "🔥 VENDER";  
      sigColor = clrRed;  
   }  
   else  
   {  
      sigText += "❌ Sin señal";  
      sigColor = clrGray;  
   }  
     
   ObjectSetString(0, g_panelPrefix + "Signal", OBJPROP_TEXT, sigText);  
   ObjectSetInteger(0, g_panelPrefix + "Signal", OBJPROP_COLOR, sigColor);  
     
   //--- Levels  
   ObjectSetString(0, g_panelPrefix + "Price", OBJPROP_TEXT,   
                   "Precio: " + DoubleToString(price, _Digits));  
   ObjectSetString(0, g_panelPrefix + "Support", OBJPROP_TEXT,   
                   "Soporte: " + DoubleToString(support, _Digits));  
   ObjectSetString(0, g_panelPrefix + "Resistance", OBJPROP_TEXT,   
                   "Resistencia: " + DoubleToString(resistance, _Digits));  
   ObjectSetString(0, g_panelPrefix + "Signals", OBJPROP_TEXT,   
                   "Señales: " + IntegerToString(g_signalCount));  
}  
//+------------------------------------------------------------------+
```