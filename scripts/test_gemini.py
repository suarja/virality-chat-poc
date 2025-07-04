from pathlib import Path
import google.generativeai as genai
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gemini_analysis.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini 2.0 Flash model
model = genai.GenerativeModel('gemini-2.0-flash')


def clean_json_string(s: str) -> str:
    """Clean a string that contains JSON by extracting only the JSON part."""
    try:
        # Find the first '{' and last '}'
        start = s.find('{')
        end = s.rfind('}') + 1
        if start >= 0 and end > start:
            return s[start:end]
        return s
    except Exception as e:
        logging.error(f"Error cleaning JSON string: {e}")
        return s


def analyze_tiktok_video(video_url: str) -> Dict[str, Any]:
    """
    Analyze a TikTok video using Gemini 2.0 Flash.

    Args:
        video_url: Direct URL to TikTok video

    Returns:
        Dictionary containing analysis results
    """

    # Test prompt for comprehensive video analysis
    prompt = """
    Analyze this TikTok video and provide a detailed analysis in the following format:

    {
        "visual_analysis": {
            "main_elements": "",
            "style_quality": "",
            "text_overlays": "",
            "transitions": ""
        },
        "content_structure": {
            "hook_effectiveness": "",
            "story_flow": "",
            "call_to_action": "",
            "organization": ""
        },
        "engagement_factors": {
            "emotional_triggers": "",
            "audience_connection": "",
            "viral_potential": "",
            "unique_points": ""
        },
        "technical_elements": {
            "length_optimization": "",
            "sound_design": "",
            "pacing": "",
            "production_quality": ""
        },
        "trend_alignment": {
            "current_trends": "",
            "hashtag_potential": "",
            "similar_content": ""
        },
        "improvement_suggestions": {
            "viral_optimization": "",
            "specific_recommendations": ""
        }
    }

    Please fill in each field with your analysis. Keep the JSON structure exactly as shown, just fill in the values.
    Ensure your response is valid JSON. Do not include any markdown formatting or code block markers.
    """

    try:
        logging.info(f"\nAnalyzing video: {video_url}")
        logging.info("Sending request to Gemini...")

        # Generate response from Gemini
        response = model.generate_content([
            {
                "text": prompt
            },
            {
                "text": f"Video URL: {video_url}\nPlease analyze this video and provide the response in the exact JSON format specified above."
            }
        ])

        logging.info("Received response from Gemini")

        # Log raw response for debugging
        raw_response = response.text
        logging.debug(f"Raw response:\n{raw_response}")

        try:
            # Clean and parse JSON
            cleaned_json = clean_json_string(raw_response)
            analysis = json.loads(cleaned_json)
            logging.info("Successfully parsed JSON response")

            return {
                'success': True,
                'analysis': analysis,
                'raw_response': raw_response,
                'timestamp': datetime.now().isoformat()
            }

        except json.JSONDecodeError as je:
            logging.error(f"Failed to parse JSON: {je}")
            return {
                'success': False,
                'error': f"JSON parsing error: {str(je)}",
                'raw_response': raw_response,
                'timestamp': datetime.now().isoformat()
            }

    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def main():
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    output_dir = Path("docs/gemini_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test videos
    test_videos = [
        "https://www.tiktok.com/@leaelui/video/7522161584643263766",
        "https://www.tiktok.com/@leaelui/video/7521405759767219478"
    ]

    logging.info("🎥 Starting Gemini Video Analysis Test\n")

    for i, video_url in enumerate(test_videos, 1):
        logging.info(f"\n📊 Analyzing Video {i}: {video_url}")
        result = analyze_tiktok_video(video_url)

        # Save complete result including raw response
        output_file = output_dir / \
            f"video_{i}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        logging.info(f"\n💾 Results saved to {output_file}")

        if result['success']:
            logging.info("\n✅ Analysis Complete!")
        else:
            logging.error(
                f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
