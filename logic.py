import re
import joblib
import os
import numpy as np
from datetime import datetime

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DiagnosticAssistant:
    def __init__(self):
        # Load Multi-Condition ML Model
        try:
            self.multi_model = joblib.load(os.path.join(BASE_DIR, 'multi_svm_model.pkl'))
            self.multi_vec = joblib.load(os.path.join(BASE_DIR, 'multi_tfidf.pkl'))
            self.has_ml = True
        except Exception as e:
            print(f"ML Load Error (Multi): {e}")
            self.has_ml = False

        # Legend for Rule-based
        self.CATEGORIES = {
            "Anxiety Disorders": [r"\bworr(y|ied|ying)\b", r"\banxious\b", r"\banxiety\b", r"\bpanic\b", r"\bfraid\b", r"\bfear\b"],
            "Mood Disorders": [r"\bdepress\w*\b", r"\bsad\w*\b", r"\bhopeless\w*\b", r"\bworthless\w*\b", r"\banhedonia\b"],
            "Stress & Trauma": [r"\btrauma\b", r"\bflashback\b", r"\bnightmare\b", r"\bstress\b", r"\boverwhelmed\b"]
        }

    def analyze(self, text):
        # 1. Rule-based analysis
        results = {}
        for cat, markers in self.CATEGORIES.items():
            count = sum(1 for m in markers if re.search(m, text, re.IGNORECASE))
            results[cat] = min(count * 20, 100)
        
        # 2. ML Inference (if available)
        ml_insights = None
        if self.has_ml and text.strip():
            try:
                vec = self.multi_vec.transform([text])
                # For SVM, we use decision_function for probability proxy
                d_func = self.multi_model.decision_function(vec)[0]
                exp_d = np.exp(d_func - np.max(d_func))
                probs = exp_d / exp_d.sum()
                
                classes = self.multi_model.classes_
                prob_map = list(zip(classes, probs))
                prob_map.sort(key=lambda x: x[1], reverse=True)
                ml_insights = prob_map
            except Exception as e:
                print(f"ML Inference Error: {e}")

        return {
            "rule_based": results,
            "ml_insights": ml_insights
        }

class SituationalAnalyzer:
    def __init__(self):
        # Load Suicide Risk ML Model
        try:
            self.suicide_model = joblib.load(os.path.join(BASE_DIR, 'suicide_svm_model.pkl'))
            self.suicide_vec = joblib.load(os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl'))
            self.has_ml = True
        except Exception as e:
            print(f"ML Load Error (Suicide): {e}")
            self.has_ml = False

    def analyze(self, text):
        # 1. Rule-based Emergency Check
        is_emergency_rule = bool(re.search(r"\bdone with life\b|\bend it\b|\bhopeless\b", text, re.IGNORECASE))
        
        # 2. ML Suicide Risk Prediction
        is_high_risk_ml = False
        confidence = 0.0
        
        if self.has_ml and text.strip():
            try:
                vec = self.suicide_vec.transform([text])
                prediction = self.suicide_model.predict(vec)[0]
                # SVM doesn't always have predict_proba, use decision_function if needed
                if hasattr(self.suicide_model, "predict_proba"):
                    probs = self.suicide_model.predict_proba(vec)[0]
                    confidence = probs[1] if prediction == 1 else probs[0]
                else:
                    d_func = self.suicide_model.decision_function(vec)[0]
                    confidence = 1 / (1 + np.exp(-d_func)) # Sigmoid for confidence proxy
                
                is_high_risk_ml = (prediction == 1)
            except Exception as e:
                print(f"ML Suicide Prediction Error: {e}")

        # Combine logic
        is_emergency = is_emergency_rule or is_high_risk_ml
        
        # Simple PoM score 
        neg_markers = [r"\bnobody\b", r"\balone\b", r"\bfailing\b", r"\bhate\b", r"\bworried\b"]
        neg_count = sum(1 for m in neg_markers if re.search(m, text, re.IGNORECASE))
        pom_score = max(100 - (neg_count * 25), 0)
        
        if is_emergency:
            pom_score = min(pom_score, 10)

        return {
            "pom_score": pom_score,
            "is_emergency": is_emergency,
            "is_ml_risk": is_high_risk_ml,
            "ml_confidence": round(float(confidence), 2)
        }
