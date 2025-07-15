from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import logging

from ..models import VideoInferenceResponse
from ..services.video_inference_service import perform_video_inference
from ..dependencies import get_current_token # Import the authentication dependency

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/infer", response_model=VideoInferenceResponse, dependencies=[Depends(get_current_token)])
async def infer_video(video_file: UploadFile = File(...)):
    """
    Performs inference on an uploaded video using a remote Hugging Face Endpoint.
    This endpoint is protected by a Bearer Token.
    """
    try:
        response = await perform_video_inference(video_file)
        return response
    except HTTPException as e:
        raise e # Re-raise HTTPException directly
    except Exception as e:
        logger.error(f"Video inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Video inference failed: {str(e)}")
