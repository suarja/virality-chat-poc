from fastapi import APIRouter, HTTPException
import logging
from ..simulation_endpoint import TikTokSimulationService, SimulationRequest, SimulationResponse
from ..feature_integration import feature_manager
from ..ml_model import ml_manager
from ..tiktok_scraper_integration import tiktok_scraper_integration

router = APIRouter()
logger = logging.getLogger(__name__)

simulation_service = TikTokSimulationService(
    feature_manager, ml_manager, tiktok_scraper_integration)

@router.post("/simulate-virality", response_model=SimulationResponse)
async def simulate_virality(request: SimulationRequest):
    try:
        return await simulation_service.simulate_virality(request)
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")
