from pathlib import Path
import google.generativeai as genai
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Pro Vision model
model = genai.GenerativeModel('gemini-pro-vision')


def analyze_tiktok_video(video_url: str) -> Dict[str, Any]:
    """
    Analyze a TikTok video using Gemini Pro Vision.

    Args:
        video_url: Direct URL to TikTok video

    Returns:
        Dictionary containing analysis results
    """

    # Test prompt for comprehensive video analysis
    prompt = """
    Analyze this TikTok video in detail. Please provide:

    1. VISUAL ANALYSIS
    - Main visual elements and scenes
    - Visual style and quality
    - Text overlays and effects
    - Transitions and editing techniques
    
    2. CONTENT STRUCTURE
    - Hook effectiveness (first 3 seconds)
    - Story/message flow
    - Call to action
    - Content organization
    
    3. ENGAGEMENT FACTORS
    - Emotional triggers
    - Audience connection points
    - Viral potential indicators
    - Unique selling points
    
    4. TECHNICAL ELEMENTS
    - Video length optimization
    - Sound design and music
    - Pacing and rhythm
    - Production quality
    
    5. TREND ALIGNMENT
    - Current TikTok trends utilized
    - Hashtag potential
    - Similar viral content patterns
    
    6. IMPROVEMENT SUGGESTIONS
    - What could make this more viral?
    - Specific enhancement recommendations
    
    Format the response as a structured JSON with these categories.
    """

    try:
        # Generate response from Gemini
        response = model.generate_content([prompt, video_url])

        # Parse and structure the response
        analysis = json.loads(response.text)

        return {
            'success': True,
            'analysis': analysis,
            'model_usage': {
                'input_tokens': response.prompt_feedback.token_count,
                'output_tokens': len(response.text.split())
            }
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    # Test videos (replace with actual viral TikTok URLs)
    test_videos = [
        "https://www.tiktok.com/@leaelui/video/7522161584643263766",
        "https://www.tiktok.com/@leaelui/video/7521405759767219478"
    ]

    print("🎥 Starting Gemini Video Analysis Test\n")

    for i, video_url in enumerate(test_videos, 1):
        print(f"\n📊 Analyzing Video {i}: {video_url}")
        result = analyze_tiktok_video(video_url)

        if result['success']:
            print("\n✅ Analysis Complete!")
            print("\nToken Usage:")
            print(f"- Input Tokens: {result['model_usage']['input_tokens']}")
            print(f"- Output Tokens: {result['model_usage']['output_tokens']}")

            # Save results to file
            output_file = f"video_{i}_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(result['analysis'], f, indent=2)
            print(f"\n💾 Results saved to {output_file}")
        else:
            print(f"\n❌ Analysis Failed: {result['error']}")


if __name__ == "__main__":
    main()
