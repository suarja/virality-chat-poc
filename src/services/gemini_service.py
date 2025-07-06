"""
🧠 Gemini Analysis Service

Service réutilisable pour l'analyse de vidéos TikTok avec Gemini AI.
Utilisé par le pipeline, l'API, et les scripts d'analyse.
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
import json
import os
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class GeminiService:
    """Service d'analyse Gemini pour les vidéos TikTok."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le service Gemini.

        Args:
            api_key: Clé API Gemini (optionnel, utilise GOOGLE_API_KEY par défaut)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Initialize Gemini 2.0 Flash model
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("✅ Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini model: {e}")
            raise

    def _clean_json_string(self, s: str) -> str:
        """Clean a string that contains JSON by extracting only the JSON part."""
        try:
            # Find the first '{' and last '}'
            start = s.find('{')
            end = s.rfind('}') + 1
            if start >= 0 and end > start:
                return s[start:end]
            return s
        except Exception as e:
            logger.error(f"Error cleaning JSON string: {e}")
            return s

    def analyze_tiktok_video(self, video_url: str) -> Dict[str, Any]:
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
            logger.info(f"🧠 Analyzing video: {video_url}")
            logger.info("📤 Sending request to Gemini...")

            # Generate response from Gemini
            response = self.model.generate_content([
                prompt,
                f"Video URL: {video_url}\nPlease analyze this video and provide the response in the exact JSON format specified above."
            ])

            logger.info("📥 Received response from Gemini")

            # Log raw response for debugging
            raw_response = response.text
            logger.debug(f"Raw response:\n{raw_response}")

            try:
                # Clean and parse JSON
                cleaned_json = self._clean_json_string(raw_response)
                analysis = json.loads(cleaned_json)
                logger.info("✅ Successfully parsed JSON response")

                return {
                    'success': True,
                    'analysis': analysis,
                    'raw_response': raw_response,
                    'timestamp': datetime.now().isoformat()
                }

            except json.JSONDecodeError as je:
                logger.error(f"❌ Failed to parse JSON: {je}")
                return {
                    'success': False,
                    'error': f"JSON parsing error: {str(je)}",
                    'raw_response': raw_response,
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"❌ Error during analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def is_available(self) -> bool:
        """Check if Gemini service is available and working."""
        try:
            # Simple test to verify the service is working
            test_result = self.analyze_tiktok_video(
                "https://www.tiktok.com/@test/video/123")
            return test_result.get('success', False)
        except Exception as e:
            logger.warning(f"⚠️ Gemini service not available: {e}")
            return False


# Global instance for easy access
_gemini_service = None


def get_gemini_service() -> Optional[GeminiService]:
    """Get or create a global Gemini service instance."""
    global _gemini_service

    if _gemini_service is None:
        try:
            _gemini_service = GeminiService()
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize Gemini service: {e}")
            return None

    return _gemini_service


def analyze_tiktok_video(video_url: str) -> Dict[str, Any]:
    """
    Convenience function to analyze a TikTok video.

    Args:
        video_url: Direct URL to TikTok video

    Returns:
        Dictionary containing analysis results
    """
    service = get_gemini_service()
    if service is None:
        return {
            'success': False,
            'error': 'Gemini service not available',
            'timestamp': datetime.now().isoformat()
        }

    return service.analyze_tiktok_video(video_url)
