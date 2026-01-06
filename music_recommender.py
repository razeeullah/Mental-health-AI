"""
Mental Peace Music Recommendation System
Maps predicted mental states to therapeutic music categories.
"""

class MusicRecommender:
    """
    Recommends music genres based on emotional regulation principles.
    """
    
    # Therapeutic mapping based on the ISO principle of music therapy
    MAPPING = {
        "Anxiety": {
            "Genre": "Ambient & Nature Sounds",
            "Tempo": "Low (60-80 BPM)",
            "Reason": "Low BPM and steady textures help lower heart rate and reduce sympathetic nervous system arousal."
        },
        "Depression": {
            "Genre": "Uplifting Acoustic / Neo-Classical",
            "Tempo": "Moderate (100-120 BPM)",
            "Reason": "Brighter tonalities and major keys can help stimulate dopamine and provide a gentle emotional lift."
        },
        "Panic Attack": {
            "Genre": "528Hz Solfeggio / Binaural Beats",
            "Tempo": "Static / Atmospheric",
            "Reason": "Focuses the brain on specific auditory frequencies, aiding in immediate sensory grounding and neural calibration."
        },
        "High Stress": {
            "Genre": "Lo-Fi Beats / Smooth Jazz",
            "Tempo": "Relaxed (70-90 BPM)",
            "Reason": "Minimal vocal presence and repetitive rhythms reduce cognitive load and auditory filtering effort."
        },
        "Stable": {
            "Genre": "Personal Favorites / Top Hits",
            "Tempo": "Variable",
            "Reason": "Reinforces existing positive emotional states through familiar neural pathways and personal connection."
        }
    }

    @staticmethod
    def get_recommendation(mental_state):
        """
        Returns a structured recommendation for a given mental state.
        """
        # Normalize input to match keys
        normalized_state = mental_state.title()
        
        # Default to Stable logic if state is unknown
        recommendation = MusicRecommender.MAPPING.get(normalized_state, MusicRecommender.MAPPING["Stable"])
        
        return {
            "Mental_State": normalized_state,
            "Recommended_Genre": recommendation["Genre"],
            "Clinical_Logic": recommendation["Reason"],
            "Tempo": recommendation["Tempo"]
        }

# Demonstration
if __name__ == "__main__":
    print("--- Mental Peace Music Recommender Demonstration ---")
    
    test_states = ["Anxiety", "Depression", "Panic Attack", "Stable"]
    
    for state in test_states:
        rec = MusicRecommender.get_recommendation(state)
        print(f"\n[Predicted State: {rec['Mental_State']}]")
        print(f"🎵 Recommends: {rec['Recommended_Genre']} ({rec['Tempo']})")
        print(f"📖 Peace Insight: {rec['Clinical_Logic']}")
