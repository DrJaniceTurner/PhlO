from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Tuple
import uuid
from datetime import datetime


class Size(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium" 
    LARGE = "Large"


class Mission(str, Enum):
    MISSION_DRIVEN = "Mission-driven"
    COMMERCIAL = "Commercial"
    NON_PROFIT = "Non-profit"
    RTO = "RTO"
    ACADEMIA = "Academia"


class Sector(str, Enum):
    CURRENT = "Current"
    PREVIOUS = "Previous"
    NEW = "New"


class Stage(str, Enum):
    STARTUP = "Startup"
    SCALEUP = "Scaleup"
    CORPORATE = "Corporate"
    MULTINATIONAL = "Multinational"


class JobOption(BaseModel):
    """Represents a job option with all attributes"""
    id: str = None
    size: Size
    mission: Mission
    sector: Sector
    stage: Stage
    
    def __init__(self, **data):
        if 'id' not in data or data['id'] is None:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)
    
    def to_string(self) -> str:
        """Convert job option to readable string"""
        return f"{self.size.value} {self.mission.value} company in {self.sector.value} sector, {self.stage.value} stage"
    
    def to_feature_vector(self) -> Dict[str, str]:
        """Convert to feature vector for ranking algorithm"""
        return {
            "size": self.size.value,
            "mission": self.mission.value, 
            "sector": self.sector.value,
            "stage": self.stage.value
        }


class ComparisonRequest(BaseModel):
    """Request model for job comparison"""
    option_a: JobOption
    option_b: JobOption
    choice: str  # "A" or "B"
    user_id: str = "default"  # For future multi-user support


class ComparisonResponse(BaseModel):
    """Response model for next comparison"""
    option_a: JobOption
    option_b: JobOption
    comparison_id: str


class RankingResponse(BaseModel):
    """Response model for attribute rankings"""
    size_preferences: Dict[str, float]
    mission_preferences: Dict[str, float]
    sector_preferences: Dict[str, float]
    stage_preferences: Dict[str, float]
    total_comparisons: int


class ComparisonRecord(BaseModel):
    """Internal model for storing comparison data"""
    id: str
    user_id: str
    option_a: JobOption
    option_b: JobOption
    choice: str
    timestamp: datetime
    
    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)