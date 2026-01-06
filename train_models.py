import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib
import os

# 1. Suicide Risk Model (Binary)
def train_suicide_risk():
    print("Training Suicide Risk Model...")
    df = pd.read_csv('Suicide_Detection.csv').head(10000) # Sample for speed
    
    # Class mapping: suicide -> 1, non-suicide -> 0
    df['label'] = df['class'].map({'suicide': 1, 'non-suicide': 0})
    
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    X = tfidf.fit_transform(df['text'].values.astype('U'))
    y = df['label']
    
    model = LinearSVC(dual=False)
    model.fit(X, y)
    
    joblib.dump(model, 'suicide_svm_model.pkl')
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    print("Suicide Risk Model saved.")

# 2. Multi-Condition Model (Synthetic Distillation)
def train_multi_condition():
    print("Training Multi-Condition Model (Distillation)...")
    # We use some normal texts from Suicide_Detection and apply rules to generate labels
    df_raw = pd.read_csv('Suicide_Detection.csv').head(5000)
    
    # Simple Rule-based labeler for training
    CATEGORIES = {
        "Anxiety": [r"\bworr(y|ied|ying)\b", r"\banxious\b", r"\banxiety\b", r"\bpanic\b"],
        "Depression": [r"\bdepress\w*\b", r"\bsad\w*\b", r"\bhopeless\w*\b", r"\bworthless\w*\b"],
        "Stress": [r"\btrauma\b", r"\bflashback\b", r"\bnightmare\b", r"\bstress\b"]
    }

    def get_label(text):
        if text is None: return "Normal"
        text = str(text).lower()
        if "suicide" in text: return "Suicide"
        for cat, markers in CATEGORIES.items():
            if any(re.search(m, text) for m in markers):
                return cat
        return "Normal"

    df_raw['label'] = df_raw['text'].apply(get_label)
    
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    X = tfidf.fit_transform(df_raw['text'].values.astype('U'))
    y = df_raw['label']
    
    model = LinearSVC(dual=False)
    model.fit(X, y)
    
    joblib.dump(model, 'multi_svm_model.pkl')
    joblib.dump(tfidf, 'multi_tfidf.pkl')
    print("Multi-Condition Model saved.")

if __name__ == "__main__":
    train_suicide_risk()
    train_multi_condition()
