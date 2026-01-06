"""
Suicide Risk Analysis System - Core Engine
Designed for mental health screening and crisis prevention.
"""

class RiskClassifier:
    """
    Classifies suicide risk based on clinical markers.
    """
    
    @staticmethod
    def classify(depression_bool, anxiety_bool, panic_bool, specialist_bool, stress_score=None):
        """
        Determines the risk level based on clinical flags.
        
        Logic:
        - High: 3 clinical indicators OR (2 indicators + specialist history)
        - Medium: 1-2 clinical indicators
        - Low: 0 indicators
        """
        indicators = sum([depression_bool, anxiety_bool, panic_bool])
        
        # High Risk Trigger
        if indicators >= 3 or (indicators >= 2 and specialist_bool):
            return "High Risk"
        # Medium Risk Trigger
        elif indicators >= 1:
            return "Medium Risk"
        # Low Risk
        else:
            return "Low Risk"

def trigger_emergency_protocol():
    """
    Automated response for high-risk detection.
    """
    protocol = {
        "warning": "🚨 CRITICAL WARNING: High Suicide Risk Detected.",
        "immediate_action": [
            "Do not stay alone.",
            "Contact a mental health professional immediately.",
            "If in immediate danger, call emergency services (e.g., 911/988)."
        ],
        "resources": {
            "National Suicide & Crisis Lifeline": "988",
            "Crisis Text Line": "Text HOME to 741741",
            "International Directory": "https://findahelpline.com"
        }
    }
    return protocol

# Demonstration
if __name__ == "__main__":
    print("--- Suicide Risk Analysis System Simulation ---")
    
    # Simulate a High Risk Profile
    user_risk = RiskClassifier.classify(depression_bool=True, anxiety_bool=True, panic_bool=True, specialist_bool=False)
    print(f"User Risk Level: {user_risk}")
    
    if user_risk == "High Risk":
        alert = trigger_emergency_protocol()
        print(f"\n{alert['warning']}")
        print("\nAction Steps:")
        for step in alert['immediate_action']:
            print(f"- {step}")
        print("\nCrisis Resources:")
        for name, num in alert['resources'].items():
            print(f"- {name}: {num}")
