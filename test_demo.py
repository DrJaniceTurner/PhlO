#!/usr/bin/env python3
"""
Demo script for the Job Preference Ranking App

This script demonstrates the complete workflow:
1. Generate random job comparisons
2. Make preference choices
3. View updated rankings
4. Reset data
"""

import requests
import json
import time
from models import JobOption, Size, Mission, Sector, Stage
import random

BASE_URL = "http://localhost:8000"

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def make_random_choice():
    """Make a random choice between A and B"""
    return random.choice(["A", "B"])

def demo_workflow():
    """Demonstrate the complete app workflow"""
    print("🎯 Job Preference Ranking App Demo")
    print("=" * 50)
    
    # 1. Check health
    print("\n1. Checking app health...")
    response = requests.get(f"{BASE_URL}/health")
    print_json(response.json())
    
    # 2. Get initial rankings
    print("\n2. Initial rankings (should be uniform)...")
    response = requests.get(f"{BASE_URL}/rankings")
    print_json(response.json())
    
    # 3. Make several comparisons
    print("\n3. Making 5 random comparisons...")
    for i in range(5):
        # Get next comparison
        response = requests.get(f"{BASE_URL}/next")
        comparison = response.json()
        
        print(f"\nComparison {i+1}:")
        print(f"Option A: {comparison['option_a']['size']} {comparison['option_a']['mission']} "
              f"company in {comparison['option_a']['sector']} sector, {comparison['option_a']['stage']} stage")
        print(f"Option B: {comparison['option_b']['size']} {comparison['option_b']['mission']} "
              f"company in {comparison['option_b']['sector']} sector, {comparison['option_b']['stage']} stage")
        
        # Make random choice
        choice = make_random_choice()
        print(f"Choice: {choice}")
        
        # Submit comparison
        comparison_data = {
            "option_a": comparison["option_a"],
            "option_b": comparison["option_b"],
            "choice": choice,
            "user_id": "demo"
        }
        
        response = requests.post(f"{BASE_URL}/compare", json=comparison_data)
        result = response.json()
        print(f"✅ Comparison recorded (Total: {result['total_comparisons']})")
        
        time.sleep(0.5)  # Small delay for readability
    
    # 4. View final rankings
    print("\n4. Final preference rankings after 5 comparisons:")
    response = requests.get(f"{BASE_URL}/rankings")
    rankings = response.json()
    
    print("\n📊 Your Inferred Preferences:")
    print("-" * 30)
    
    for category, prefs in rankings.items():
        if category != "total_comparisons":
            print(f"\n{category.replace('_preferences', '').title()}:")
            sorted_prefs = sorted(prefs.items(), key=lambda x: x[1], reverse=True)
            for rank, (attr, score) in enumerate(sorted_prefs, 1):
                print(f"  {rank}. {attr}: {score:.1%}")
    
    print(f"\nBased on {rankings['total_comparisons']} comparisons")
    
    # 5. Reset data
    print("\n5. Resetting all data...")
    response = requests.post(f"{BASE_URL}/reset")
    print(response.json()["message"])
    
    # 6. Verify reset
    print("\n6. Verifying reset (should be uniform again)...")
    response = requests.get(f"{BASE_URL}/rankings")
    rankings = response.json()
    print(f"Total comparisons after reset: {rankings['total_comparisons']}")
    
    print("\n✨ Demo completed successfully!")
    print(f"Visit {BASE_URL} in your browser to try the interactive interface!")

if __name__ == "__main__":
    try:
        demo_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the app.")
        print("Make sure the server is running with:")
        print("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"❌ Error: {e}")