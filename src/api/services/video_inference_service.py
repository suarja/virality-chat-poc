import base64
import time
import logging
import os
import httpx
import json
from fastapi import UploadFile, HTTPException
import google.generativeai as genai

from ..models import VideoInferenceResponse

logger = logging.getLogger(__name__)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# --- Configure Gemini ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    logger.warning(
        "GEMINI_API_KEY not set. Gemini post-processing will be skipped.")
    gemini_model = None


async def perform_video_inference(video_file: UploadFile) -> VideoInferenceResponse:
    start_time = time.time()

    # Lire les variables d'environnement ici, juste avant leur utilisation
    HF_INFERENCE_ENDPOINT_URL = os.getenv("HF_INFERENCE_ENDPOINT_URL")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN")

    # Le prompt détaillé pour guider le modèle SmolVLM
    smolvlm_prompt = """
    Analyze this video and provide comprehensive metadata in the following JSON format:

    {
      "title": "A concise, descriptive title for the video (3-8 words)",
      "description": "A detailed description of what happens in the video (1-3 sentences)",
      "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
      "segments": [
        {
          "start_time": "00:00",
          "end_time": "00:15",
          "content_type": "intro|main_content|transition|outro",
          "description": "What happens in this segment",
          "visual_elements": ["person", "screen", "text", "animation"],
          "key_points": ["point1", "point2"]
        }
      ],
      "structure": {
        "has_hook": true|false,
        "has_call_to_action": true|false,
        "transitions_count": 0,
        "pacing": "fast|medium|slow"
      },
      "content_type": "tutorial|entertainment|educational|product_demo|interview|vlog|other",
      "language": "fr|en|es|de|other",
      "duration_category": "short|medium|long",
      "key_moments": {
        "hook_start": "00:05",
        "main_content_start": "00:15",
        "call_to_action_start": "01:45",
        "end": "02:00"
      }
    }

    Guidelines:
    - Title: 3-8 words, descriptive but concise
    - Description: 1-3 sentences explaining main content
    - Tags: 3-8 relevant keywords for filtering
    - Segments: Divide video into logical parts (15-30 second segments)
    - Content type: Match primary purpose of video
    - Language: Primary language spoken
    - Visual elements: What's visible (person, screen, text, etc.)
    - Key points: Main ideas or actions in each segment
    - Structure: Detect hooks, CTAs, transitions, pacing
    - Key moments: Important timestamps for future editing

    Return ONLY valid JSON. Do not include any markdown formatting or additional text.
    """

    if not HF_INFERENCE_ENDPOINT_URL or not HF_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Hugging Face Inference Endpoint is not configured on the server. Please set HF_INFERENCE_ENDPOINT_URL and HF_API_TOKEN environment variables."
        )

    try:
        video_content = await video_file.read()
        encoded_video = base64.b64encode(video_content).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": smolvlm_prompt},
                    {"type": "video", "data": encoded_video}
                ]
            }
        ]

        payload = {
            "inputs": messages,
            "parameters": {
                "max_new_tokens": 1024 # Augmenté pour permettre une sortie JSON plus longue
            }
        }

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(HF_INFERENCE_ENDPOINT_URL, json=payload, headers=headers, timeout=300.0)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
            smolvlm_raw_response = response.json()
        
        smolvlm_result_text = smolvlm_raw_response.get("generated_text", "No text generated.")

        # --- Post-traitement avec Gemini ---
        if gemini_model:
            gemini_prompt = f"""
            The following text describes a video. Convert this description into a JSON object 
            following the exact structure and guidelines provided below. 
            Ensure the output is ONLY valid JSON, with no markdown or extra text.

            Video Description: {smolvlm_result_text}

            JSON Format:
            {{
              "title": "A concise, descriptive title for the video (3-8 words)",
              "description": "A detailed description of what happens in the video (1-3 sentences)",
              "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
              "segments": [
                {{
                  "start_time": "00:00",
                  "end_time": "00:15",
                  "content_type": "intro|main_content|transition|outro",
                  "description": "What happens in this segment",
                  "visual_elements": ["person", "screen", "text", "animation"],
                  "key_points": ["point1", "point2"]
                }}
              ],
              "structure": {{
                "has_hook": true|false,
                "has_call_to_action": true|false,
                "transitions_count": 0,
                "pacing": "fast|medium|slow"
              }},
              "content_type": "tutorial|entertainment|educational|product_demo|interview|vlog|other",
              "language": "fr|en|es|de|other",
              "duration_category": "short|medium|long",
              "key_moments": {{
                "hook_start": "00:05",
                "main_content_start": "00:15",
                "call_to_action_start": "01:45",
                "end": "02:00"
              }}
            }}

            Guidelines:
            - Title: 3-8 words, descriptive but concise
            - Description: 1-3 sentences explaining main content
            - Tags: 3-8 relevant keywords for filtering
            - Segments: Divide video into logical parts (15-30 second segments)
            - Content type: Match primary purpose of video
            - Language: Primary language spoken
            - Visual elements: What's visible (person, screen, text, etc.)
            - Key points: Main ideas or actions in each segment
            - Structure: Detect hooks, CTAs, transitions, pacing
            - Key moments: Important timestamps for future editing

            Return ONLY valid JSON. Do not include any markdown formatting or additional text.
            """
            try:
                gemini_response = gemini_model.generate_content(gemini_prompt)
                # Tente de parser la réponse de Gemini comme du JSON
                try:
                    json_output = json.loads(gemini_response.text)
                    result_text = json.dumps(json_output, indent=2) # Formate joliment le JSON
                except json.JSONDecodeError:
                    logger.warning("Gemini did not return valid JSON. Returning raw text.")
                    result_text = gemini_response.text
            except Exception as e:
                logger.error(f"Gemini post-processing error: {e}")
                result_text = smolvlm_result_text # Retourne le résultat brut de SmolVLM en cas d'erreur Gemini
        else:
            result_text = smolvlm_result_text # Pas de Gemini, retourne le résultat brut de SmolVLM

    except httpx.RequestError as e:
        logger.error(f"HTTP request error to Hugging Face Inference Endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed due to network error: {str(e)}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP status error from Hugging Face Inference Endpoint: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Inference failed with HTTP error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error(f"Hugging Face inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

    end_time = time.time()
    inference_time = end_time - start_time
    print(f"Remote inference time: {inference_time:.2f} seconds")
    return VideoInferenceResponse(result=result_text, inference_time=inference_time)

