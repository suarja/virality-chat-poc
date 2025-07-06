# 🚀 TikTok Virality Prediction API

## 🎯 Overview

This API provides two main types of TikTok virality analysis:

1. **📊 Analysis Endpoints** - Analyze existing videos with real post-publication data
2. **🎯 Simulation Endpoints** - Simulate pre-publication scenarios for planning

## 🔄 Analysis vs Simulation: Key Differences

### **📊 Analysis Endpoints (Post-Publication Data)**

**Use Case**: "Why did this video go viral?"

- ✅ **Uses real engagement data** (views, likes, comments, shares)
- ✅ **Analyzes existing videos** that have already been published
- ✅ **Explains current performance** with feature importance
- ✅ **Provides actionable insights** for future content
- ✅ **Caching supported** for efficiency

**Example**: "Why did @swarecito's ChatGPT video get 53k views?"

### **🎯 Simulation Endpoints (Pre-Publication Scenarios)**

**Use Case**: "When should I publish this video for maximum virality?"

- ✅ **Simulates pre-publication scenarios** (no real engagement data)
- ✅ **Tests different publication times** and hashtag strategies
- ✅ **Predicts optimal conditions** for viral potential
- ✅ **Provides planning recommendations** for content creators
- ✅ **Caching supported** for base video data only

**Example**: "When should I publish my new video for maximum virality?"

## 📊 Analysis Endpoints

### **Analyze Single Video**

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true
  }'
```

**What you get**:

- ✅ Current virality score (0.75 = 75% viral potential)
- ✅ Real engagement data (views, likes, comments)
- ✅ Feature importance analysis
- ✅ Specific improvement recommendations
- ✅ Caching information (`cache_used: true`)

### **Analyze Profile**

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "swarecito",
    "max_videos": 10,
    "use_cache": true
  }'
```

**What you get**:

- ✅ Profile-level virality analysis
- ✅ Multiple video comparison
- ✅ Content pattern insights
- ✅ Audience engagement trends

## 🎯 Simulation Endpoints

### **Simulate Publication Scenarios**

```bash
curl -X POST "http://localhost:8000/simulate-virality" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true,
    "scenarios": [
      {
        "name": "Morning Publication",
        "description": "Publish at 9am on Monday",
        "publication_hour": 9,
        "publication_day": "monday",
        "hashtags": ["fyp", "viral", "trending"],
        "engagement_multiplier": 1.2
      },
      {
        "name": "Evening Publication",
        "description": "Publish at 8pm on Friday",
        "publication_hour": 20,
        "publication_day": "friday",
        "hashtags": ["fyp", "comedy", "funny"],
        "engagement_multiplier": 1.5
      }
    ],
    "simulation_count": 5
  }'
```

**What you get**:

- ✅ Best publication time recommendations
- ✅ Optimal hashtag combinations
- ✅ Expected virality improvement
- ✅ Content optimization suggestions
- ✅ Multiple scenario comparisons
- ✅ Caching information (`cache_used: true`)

## 🔧 Caching System

### **How Caching Works**

Both endpoints support caching for efficiency:

```json
{
  "cache_used": true,
  "simulation_type": "pre_publication" // Only for simulation
}
```

### **Analysis Endpoint Caching**

- ✅ Caches complete video data (content + engagement)
- ✅ Avoids repeated scraping of same videos
- ✅ Returns `cache_used: true` when using cached data

### **Simulation Endpoint Caching**

- ✅ Caches base video data (content only, no engagement)
- ✅ Uses cached data for content analysis
- ✅ Simulates scenarios without real engagement data
- ✅ Returns `cache_used: true` when using cached data

## 📈 Score Interpretation

### **Virality Score (0-1)**

- **0.0-0.3**: Low viral potential
- **0.3-0.6**: Moderate viral potential
- **0.6-0.8**: High viral potential
- **0.8-1.0**: Very high viral potential

### **Confidence Score (0-1)**

- **0.0-0.5**: Low confidence in prediction
- **0.5-0.8**: Moderate confidence
- **0.8-1.0**: High confidence

### **R² Score (0-1)**

- **0.457**: Our model explains 45.7% of viral variance
- **Industry standard**: 0.4+ is considered good for social media prediction

## 🚀 Quick Start

### **1. Start the API**

```bash
cd src
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Test Analysis (Post-Publication)**

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true
  }'
```

### **3. Test Simulation (Pre-Publication)**

```bash
curl -X POST "http://localhost:8000/simulate-virality" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true,
    "scenarios": [
      {
        "name": "Test Scenario",
        "description": "Test publication scenario",
        "publication_hour": 12,
        "publication_day": "monday",
        "hashtags": ["fyp", "viral"],
        "engagement_multiplier": 1.0
      }
    ],
    "simulation_count": 3
  }'
```

## 📚 Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🎯 When to Use Each Endpoint

### **Use Analysis When:**

- ✅ You have an existing TikTok video
- ✅ You want to understand why it went viral (or didn't)
- ✅ You want to analyze real engagement data
- ✅ You're doing competitive research

### **Use Simulation When:**

- ✅ You're planning to publish a video
- ✅ You want to optimize publication timing
- ✅ You want to test different hashtag strategies
- ✅ You want to predict virality before publishing

## 🔧 Technical Details

### **Pre-Publication Features (Simulation)**

- ✅ Video duration and format
- ✅ Publication timing (hour, day)
- ✅ Hashtag strategy
- ✅ Content features (overlays, transitions, CTA)
- ✅ Engagement multipliers (simulated)

### **Post-Publication Features (Analysis)**

- ✅ Real view counts
- ✅ Real like counts
- ✅ Real comment counts
- ✅ Real share counts
- ✅ Engagement ratios
- ✅ Growth patterns

### **No Post-Publication Data Used in Simulation:**

- ❌ Real view counts
- ❌ Real like counts
- ❌ Real comment counts
- ❌ Real share counts

This ensures true pre-publication simulation without bias from existing performance data.

---

**Version**: 1.0.0  
**Last Updated**: January 6, 2025  
**Status**: ✅ Production Ready
