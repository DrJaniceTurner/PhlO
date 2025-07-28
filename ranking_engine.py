"""
Ranking Engine Module - Isolated for easy swapping of algorithms

This module handles preference inference from pairwise comparisons.
Currently uses choix library but designed to be easily swappable
with BradleyTerryScalable or other ranking algorithms.
"""

import choix
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from models import ComparisonRecord, JobOption, Size, Mission, Sector, Stage


class RankingEngine:
    """
    Handles preference inference from pairwise comparison data.
    
    Uses choix library to implement Bradley-Terry model for ranking
    job attributes based on user choices.
    """
    
    def __init__(self):
        self.comparisons = []
        
    def add_comparison(self, record: ComparisonRecord):
        """Add a comparison record to the dataset"""
        self.comparisons.append(record)
    
    def clear_comparisons(self):
        """Clear all comparison data"""
        self.comparisons = []
    
    def get_attribute_rankings(self, user_id: str = "default") -> Dict[str, Dict[str, float]]:
        """
        Calculate preference rankings for each attribute category.
        
        Returns normalized preference scores for each attribute value,
        where higher scores indicate stronger preference.
        """
        user_comparisons = [c for c in self.comparisons if c.user_id == user_id]
        
        if len(user_comparisons) < 2:
            # Not enough data for meaningful rankings
            return self._get_default_rankings()
        
        rankings = {}
        
        # Calculate rankings for each attribute type
        for attr_name in ["size", "mission", "sector", "stage"]:
            attr_rankings = self._calculate_attribute_ranking(user_comparisons, attr_name)
            rankings[f"{attr_name}_preferences"] = attr_rankings
            
        return rankings
    
    def _calculate_attribute_ranking(self, comparisons: List[ComparisonRecord], 
                                   attribute: str) -> Dict[str, float]:
        """
        Calculate ranking for a specific attribute using choix library.
        
        For each comparison, we extract the attribute values and determine
        which was preferred based on the user's choice.
        """
        # Map attribute values to indices
        attr_values = self._get_attribute_values(attribute)
        value_to_idx = {val: idx for idx, val in enumerate(attr_values)}
        
        # Prepare data for choix
        comparison_data = []
        
        for record in comparisons:
            # Get attribute values for both options
            val_a = getattr(record.option_a, attribute).value
            val_b = getattr(record.option_b, attribute).value
            
            # Skip if both options have same attribute value
            if val_a == val_b:
                continue
                
            idx_a = value_to_idx[val_a]
            idx_b = value_to_idx[val_b]
            
            # Determine winner based on choice
            if record.choice == "A":
                winner = idx_a
                loser = idx_b
            else:  # choice == "B"
                winner = idx_b
                loser = idx_a
                
            comparison_data.append((winner, loser))
        
        if len(comparison_data) < 2:
            # Not enough data for this attribute
            return self._get_uniform_scores(attr_values)
        
        try:
            # Use choix to estimate Bradley-Terry parameters
            n_items = len(attr_values)
            params = choix.ilsr_pairwise(n_items, comparison_data, alpha=0.01)
            
            # Convert to normalized probabilities (softmax)
            scores = np.exp(params)
            scores = scores / np.sum(scores)
            
            # Return as dictionary
            return {attr_values[i]: float(scores[i]) for i in range(len(attr_values))}
            
        except Exception as e:
            print(f"Error calculating rankings for {attribute}: {e}")
            return self._get_uniform_scores(attr_values)
    
    def _get_attribute_values(self, attribute: str) -> List[str]:
        """Get all possible values for an attribute"""
        if attribute == "size":
            return [e.value for e in Size]
        elif attribute == "mission":
            return [e.value for e in Mission]
        elif attribute == "sector":
            return [e.value for e in Sector]
        elif attribute == "stage":
            return [e.value for e in Stage]
        else:
            raise ValueError(f"Unknown attribute: {attribute}")
    
    def _get_uniform_scores(self, values: List[str]) -> Dict[str, float]:
        """Return uniform scores when insufficient data"""
        score = 1.0 / len(values)
        return {val: score for val in values}
    
    def _get_default_rankings(self) -> Dict[str, Dict[str, float]]:
        """Return default uniform rankings when no data available"""
        return {
            "size_preferences": self._get_uniform_scores([e.value for e in Size]),
            "mission_preferences": self._get_uniform_scores([e.value for e in Mission]),
            "sector_preferences": self._get_uniform_scores([e.value for e in Sector]),
            "stage_preferences": self._get_uniform_scores([e.value for e in Stage])
        }
    
    def get_total_comparisons(self, user_id: str = "default") -> int:
        """Get total number of comparisons for a user"""
        return len([c for c in self.comparisons if c.user_id == user_id])


# Global instance - in production, this would be properly managed
ranking_engine = RankingEngine()