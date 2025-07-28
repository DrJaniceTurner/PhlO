"""
Job Option Generator

Utility functions for creating random job options for pairwise comparisons.
Ensures variety and avoids duplicate comparisons.
"""

import random
import uuid
from typing import Tuple
from models import JobOption, Size, Mission, Sector, Stage


class JobGenerator:
    """Generates random job options for comparison"""
    
    def __init__(self):
        # Keep track of recent comparisons to avoid immediate duplicates
        self.recent_comparisons = []
        self.max_recent = 20  # Remember last 20 comparisons
        
    def generate_comparison_pair(self) -> Tuple[JobOption, JobOption]:
        """
        Generate two different job options for comparison.
        
        Ensures the options are meaningfully different and haven't
        been compared recently.
        """
        max_attempts = 50  # Prevent infinite loops
        attempts = 0
        
        while attempts < max_attempts:
            option_a = self._generate_random_job()
            option_b = self._generate_random_job()
            
            # Ensure options are different
            if self._are_jobs_different(option_a, option_b):
                # Check if this comparison was recent
                comparison_key = self._get_comparison_key(option_a, option_b)
                if comparison_key not in self.recent_comparisons:
                    # Add to recent comparisons
                    self.recent_comparisons.append(comparison_key)
                    if len(self.recent_comparisons) > self.max_recent:
                        self.recent_comparisons.pop(0)
                    
                    return option_a, option_b
            
            attempts += 1
        
        # Fallback: just return two different jobs even if recently compared
        option_a = self._generate_random_job()
        option_b = self._generate_random_job()
        while not self._are_jobs_different(option_a, option_b):
            option_b = self._generate_random_job()
            
        return option_a, option_b
    
    def _generate_random_job(self) -> JobOption:
        """Generate a single random job option"""
        return JobOption(
            id=str(uuid.uuid4()),
            size=random.choice(list(Size)),
            mission=random.choice(list(Mission)),
            sector=random.choice(list(Sector)),
            stage=random.choice(list(Stage))
        )
    
    def _are_jobs_different(self, job_a: JobOption, job_b: JobOption) -> bool:
        """Check if two jobs have at least one different attribute"""
        return (job_a.size != job_b.size or 
                job_a.mission != job_b.mission or
                job_a.sector != job_b.sector or
                job_a.stage != job_b.stage)
    
    def _get_comparison_key(self, job_a: JobOption, job_b: JobOption) -> str:
        """
        Generate a normalized key for comparison tracking.
        
        Ensures that (A,B) and (B,A) are treated as the same comparison.
        """
        # Create sorted tuple of job representations to normalize order
        job_a_str = f"{job_a.size.value}|{job_a.mission.value}|{job_a.sector.value}|{job_a.stage.value}"
        job_b_str = f"{job_b.size.value}|{job_b.mission.value}|{job_b.sector.value}|{job_b.stage.value}"
        
        # Sort to ensure consistent ordering
        return "|".join(sorted([job_a_str, job_b_str]))
    
    def reset(self):
        """Clear recent comparison history"""
        self.recent_comparisons = []


# Global generator instance
job_generator = JobGenerator()