# TikTok Video Feature Engineering

This document describes our approach to feature engineering for TikTok video virality prediction.

## Overview

Our feature engineering pipeline combines three main data sources:

1. Raw TikTok video metadata
2. Gemini AI content analysis
3. Derived features and metrics

## Feature Categories

### Basic Video Features

- `video_id`: Unique video identifier
- `title`: Video title
- `description`: Video description
- `duration`: Video duration in seconds
- `post_time`: Time of posting
- `extraction_time`: Time of data extraction

### Engagement Metrics

- `view_count`: Number of views
- `like_count`: Number of likes
- `comment_count`: Number of comments
- `share_count`: Number of shares
- `like_rate`: Likes per view
- `comment_rate`: Comments per view
- `share_rate`: Shares per view
- `engagement_rate`: Overall engagement rate

### Content Features

- `hashtags`: List of hashtags used
- `hashtag_count`: Number of hashtags
- `music_info`: Music information (title, author, duration, originality)

### Temporal Features

- `hour_of_day`: Hour when posted (0-23)
- `day_of_week`: Day of week posted (0-6)
- `month`: Month posted (1-12)
- `is_weekend`: Whether posted on weekend
- `is_business_hours`: Whether posted during business hours (9-17)

### Gemini Analysis Features

#### Visual Analysis

- `has_text_overlays`: Whether video has text overlays
- `has_transitions`: Whether video has transitions
- `visual_quality_score`: Quality score for visual elements (0-1)

#### Content Structure

- `has_hook`: Effectiveness of video hook (0-1)
- `has_story`: Whether video has narrative structure
- `has_call_to_action`: Whether video has explicit CTA

#### Engagement Factors

- `viral_potential_score`: Estimated viral potential (0-1)
- `emotional_trigger_count`: Number of emotional triggers
- `audience_connection_score`: Audience connection strength (0-1)

#### Technical Elements

- `length_optimized`: Whether video length is optimized
- `sound_quality_score`: Quality score for sound (0-1)
- `production_quality_score`: Overall production quality (0-1)

#### Trend Alignment

- `trend_alignment_score`: How well content aligns with trends (0-1)
- `estimated_hashtag_count`: Estimated optimal hashtag count

## Feature Extraction Process

1. **Raw Data Processing**

   - Extract basic video metadata
   - Calculate engagement metrics
   - Process temporal information
   - Parse content elements (hashtags, music)

2. **Gemini Analysis Integration**

   - Process AI analysis of video content
   - Extract qualitative assessments
   - Convert text descriptions to numerical scores
   - Identify key content characteristics

3. **Feature Normalization**
   - Scale numerical features
   - Encode categorical variables
   - Handle missing values
   - Validate against schema

## Usage

See the following notebooks for examples:

- `notebooks/01_feature_extraction_demo.ipynb`: Basic feature extraction
- `notebooks/02_data_processing_demo.ipynb`: Full data processing pipeline

## Feature Validation

Features are validated through:

1. Schema validation using Pydantic
2. Range checks for numerical values
3. Format validation for temporal data
4. Completeness checks for required fields

## Metadata Tracking

For each processed video, we track:

- Extraction timestamp
- Features successfully extracted
- Processing duration
- Validation status
- Error messages (if any)

## Dependencies

Required packages:

- numpy>=1.24.0
- pandas>=2.0.0
- pydantic>=2.0.0
- scikit-learn>=1.3.0

## Future Improvements

1. **Additional Features**

   - Audio analysis features
   - Visual content analysis (colors, composition)
   - User interaction patterns
   - Cross-platform metrics

2. **Feature Selection**

   - Correlation analysis
   - Feature importance ranking
   - Dimensionality reduction
   - A/B testing of feature sets

3. **Performance Optimization**
   - Batch processing
   - Parallel processing
   - Caching mechanisms
   - Incremental updates
