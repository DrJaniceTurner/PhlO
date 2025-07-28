"""
Job Preference Ranking API

FastAPI application that handles pairwise job comparisons and infers
user preferences using the choix library.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid
from typing import Dict

from models import (
    ComparisonRequest, ComparisonResponse, RankingResponse, 
    ComparisonRecord, JobOption
)
from ranking_engine import RankingEngine
from job_generator import JobGenerator

# Initialize global instances
ranking_engine = RankingEngine()
job_generator = JobGenerator()

# Initialize FastAPI app
app = FastAPI(
    title="Job Preference Ranking API",
    description="API for inferring job preferences from pairwise comparisons",
    version="1.0.0"
)

# Set up templates for simple HTML frontend
templates = Jinja2Templates(directory="templates")

# In-memory storage for active comparisons
active_comparisons: Dict[str, ComparisonResponse] = {}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main comparison interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/rankings", response_model=RankingResponse)
async def get_rankings(user_id: str = "default"):
    """
    Get current preference rankings for a user.
    
    Returns normalized preference scores for each attribute category.
    Higher scores indicate stronger preference.
    """
    try:
        rankings = ranking_engine.get_attribute_rankings(user_id)
        total_comparisons = ranking_engine.get_total_comparisons(user_id)
        
        return RankingResponse(
            size_preferences=rankings["size_preferences"],
            mission_preferences=rankings["mission_preferences"],
            sector_preferences=rankings["sector_preferences"],
            stage_preferences=rankings["stage_preferences"],
            total_comparisons=total_comparisons
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating rankings: {str(e)}")


@app.get("/next", response_model=ComparisonResponse)
async def get_next_comparison():
    """
    Generate two random job options for comparison.
    
    Returns a comparison with unique ID that can be referenced
    when submitting the user's choice.
    """
    try:
        # Generate two different job options
        option_a, option_b = job_generator.generate_comparison_pair()
        
        # Create comparison response with unique ID
        comparison_id = str(uuid.uuid4())
        comparison = ComparisonResponse(
            option_a=option_a,
            option_b=option_b,
            comparison_id=comparison_id
        )
        
        # Store for reference when user submits choice
        active_comparisons[comparison_id] = comparison
        
        return comparison
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comparison: {str(e)}")


@app.post("/compare")
async def submit_comparison(request: ComparisonRequest):
    """
    Submit a user's choice between two job options.
    
    Stores the comparison data and updates preference rankings.
    Choice should be "A" or "B".
    """
    try:
        # Validate choice
        if request.choice not in ["A", "B"]:
            raise HTTPException(status_code=400, detail="Choice must be 'A' or 'B'")
        
        # Create comparison record
        record = ComparisonRecord(
            user_id=request.user_id,
            option_a=request.option_a,
            option_b=request.option_b,
            choice=request.choice
        )
        
        # Add to ranking engine
        ranking_engine.add_comparison(record)
        
        return {
            "status": "success",
            "message": "Comparison recorded successfully",
            "comparison_id": record.id,
            "total_comparisons": ranking_engine.get_total_comparisons(request.user_id)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording comparison: {str(e)}")


@app.post("/reset")
async def reset_data(user_id: str = "default"):
    """
    Reset all comparison data for a user.
    
    Clears all stored comparisons and resets preference rankings.
    Useful for starting fresh or testing.
    """
    try:
        # Clear ranking engine data
        ranking_engine.clear_comparisons()
        
        # Clear job generator history
        job_generator.reset()
        
        # Clear active comparisons
        active_comparisons.clear()
        
        return {
            "status": "success",
            "message": "All data reset successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting data: {str(e)}")


@app.get("/rankings-page", response_class=HTMLResponse)
async def rankings_page(request: Request):
    """Serve the rankings display page"""
    return templates.TemplateResponse("rankings.html", {"request": request})


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "total_comparisons": ranking_engine.get_total_comparisons(),
        "active_comparisons": len(active_comparisons)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)