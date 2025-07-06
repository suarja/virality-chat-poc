# 🚀 TikTok Virality Prediction API

## 📋 Overview

This API provides TikTok virality prediction capabilities with two main approaches:

1. **📊 Analysis Endpoints** - Analyze existing TikTok videos (post-publication data)
2. **🎯 Simulation Endpoints** - Predict virality for pre-publication scenarios

## 🔗 API Endpoints

### **📊 Analysis Endpoints (Post-Publication)**

#### `/analyze-tiktok-url`

Analyzes an existing TikTok video using real engagement data.

**Use Case**: "How viral is this existing video and why?"

**Request**:

```json
{
  "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
  "use_cache": true
}
```

**Response**:

```json
{
  "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
  "video_data": {
    "playCount": 53000,
    "diggCount": 1916,
    "commentCount": 631,
    "shareCount": 302,
    "collectCount": 1807,
    "hashtags": ["chatgpt", "agent", "prompt", "instruction"]
  },
  "prediction": {
    "virality_score": 0.75,
    "confidence": 0.85,
    "r2_score": 0.457,
    "recommendations": [
      "Optimize publication timing (6-8am, 12-2pm, 6-8pm hours)",
      "Reduce hashtag count (less is better)",
      "Add more visual contact with camera"
    ]
  },
  "cache_used": true,
  "status": "completed"
}
```

**What this tells you**:

- ✅ **Current virality score** (0.75 = 75% viral potential)
- ✅ **Why it's viral** (feature importance analysis)
- ✅ **How to improve** (specific recommendations)
- ✅ **Real engagement data** (views, likes, comments, shares)

#### `/analyze-tiktok-profile`

Analyzes multiple videos from a TikTok profile.

**Use Case**: "What makes this creator's videos viral?"

### **🎯 Simulation Endpoints (Pre-Publication)**

#### `/simulate-virality`

Simulates different publication scenarios for a video.

**Use Case**: "When should I publish this video for maximum virality?"

**Request**:

```json
{
  "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
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
}
```

**Response**:

```json
{
  "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
  "original_virality_score": 0.75,
  "scenarios": [
    {
      "scenario_name": "Morning Publication",
      "average_virality_score": 0.82,
      "best_virality_score": 0.89,
      "recommendations": [
        "Publish at optimal hours: 9, 12, 18, 21h",
        "Add trending hashtags for better reach"
      ]
    },
    {
      "scenario_name": "Evening Publication",
      "average_virality_score": 0.91,
      "best_virality_score": 0.95,
      "recommendations": [
        "Friday evening is optimal for this content type",
        "Consider adding call-to-action for engagement"
      ]
    }
  ],
  "best_scenario": "Evening Publication",
  "best_score": 0.91
}
```

**What this tells you**:

- ✅ **Best publication time** (Friday 8pm)
- ✅ **Expected virality improvement** (0.75 → 0.91)
- ✅ **Optimal hashtags** for your content
- ✅ **Engagement strategies** to maximize reach

## 🔄 Analysis vs Simulation: When to Use What?

### **📊 Use Analysis Endpoints When:**

- ✅ You have an existing TikTok video
- ✅ You want to understand why it went viral (or didn't)
- ✅ You want to analyze real engagement data
- ✅ You're doing competitor research

**Example**: "Why did @swarecito's ChatGPT video get 53k views?"

### **🎯 Use Simulation Endpoints When:**

- ✅ You're planning to publish a video
- ✅ You want to optimize publication timing
- ✅ You want to test different hashtag strategies
- ✅ You want to predict virality before publishing

**Example**: "When should I publish my new video for maximum virality?"

## 📈 Understanding the Response

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

### **1. Analyze an Existing Video**

```bash
curl -X POST "http://localhost:8000/analyze-tiktok-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "use_cache": true
  }'
```

### **2. Simulate Publication Scenarios**

```bash
curl -X POST "http://localhost:8000/simulate-virality" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.tiktok.com/@swarecito/video/7505706702050823446",
    "scenarios": [
      {
        "name": "Optimal Timing",
        "publication_hour": 9,
        "publication_day": "monday",
        "hashtags": ["fyp", "viral"]
      }
    ]
  }'
```

## 🔧 Configuration

### **Environment Variables**

```bash
APIFY_API_TOKEN=your_apify_token  # For TikTok scraping
RAILWAY_ENVIRONMENT=production     # For deployment
```

### **Caching**

- **`use_cache: true`**: Use cached data (faster, no scraping)
- **`use_cache: false`**: Always scrape fresh data (slower, up-to-date)

## 📚 API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🎯 Production Usage

### **For Content Creators**

1. Use `/simulate-virality` to plan your next video
2. Use `/analyze-tiktok-url` to understand your best-performing content
3. Follow the recommendations to optimize future videos

### **For Agencies**

1. Use `/analyze-tiktok-profile` to analyze client accounts
2. Use `/simulate-virality` to create content strategies
3. Track performance improvements over time

### **For Researchers**

1. Use analysis endpoints for data collection
2. Use simulation endpoints for hypothesis testing
3. Export data for further analysis

---

**Version**: 1.0.0  
**Last Updated**: January 6, 2025  
**Status**: ✅ Production Ready
