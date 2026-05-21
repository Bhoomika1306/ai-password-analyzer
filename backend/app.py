# ============================================
# app.py - Flask API with ML Prediction (Vercel)
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

# Create Flask app
app = Flask(__name__)

# Allow all origins (Vercel handles CORS at edge)
CORS(app)


# ============================================
# LOAD THE TRAINED MODEL
# ============================================

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model.pkl')

try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# ============================================
# FEATURE EXTRACTION
# ============================================

def extract_features(password):
    features = {
        'length': len(password),
        'uppercase_count': sum(1 for c in password if c.isupper()),
        'lowercase_count': sum(1 for c in password if c.islower()),
        'digit_count': sum(1 for c in password if c.isdigit()),
        'symbol_count': sum(1 for c in password if not c.isalnum()),
        'unique_chars': len(set(password)),
        'unique_ratio': len(set(password)) / len(password) if len(password) > 0 else 0,
        'repeated_chars': len(password) - len(set(password)),
    }
    return features


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_strength_label(prediction):
    labels = {0: 'Weak', 1: 'Medium', 2: 'Strong'}
    return labels.get(prediction, 'Unknown')

def get_risk_level(strength):
    risk_map = {'Weak': 'High', 'Medium': 'Medium', 'Strong': 'Low'}
    return risk_map.get(strength, 'Unknown')

def calculate_score(features, strength):
    score = 0
    
    if features['length'] >= 12: score += 30
    elif features['length'] >= 8: score += 20
    elif features['length'] >= 6: score += 10
    else: score += 5
    
    if features['uppercase_count'] > 0: score += 10
    if features['lowercase_count'] > 0: score += 10
    if features['digit_count'] > 0: score += 10
    if features['symbol_count'] > 0: score += 10
    
    if features['unique_ratio'] > 0.8: score += 20
    elif features['unique_ratio'] > 0.6: score += 15
    elif features['unique_ratio'] > 0.4: score += 10
    else: score += 5
    
    if features['repeated_chars'] == 0: score += 10
    elif features['repeated_chars'] <= 2: score += 5
    
    if strength == 'Weak': score = min(score, 40)
    elif strength == 'Medium': score = min(max(score, 41), 70)
    else: score = max(score, 71)
    
    return min(score, 100)

def generate_suggestions(features, strength):
    suggestions = []
    
    if features['length'] < 8:
        suggestions.append("Make your password at least 8 characters long")
    elif features['length'] < 12:
        suggestions.append("Consider using 12+ characters for better security")
    if features['uppercase_count'] == 0:
        suggestions.append("Add uppercase letters (A-Z)")
    if features['lowercase_count'] == 0:
        suggestions.append("Add lowercase letters (a-z)")
    if features['digit_count'] == 0:
        suggestions.append("Add numbers (0-9)")
    if features['symbol_count'] == 0:
        suggestions.append("Add special symbols (!@#$%^&*)")
    if features['repeated_chars'] > 2:
        suggestions.append("Avoid repeating characters")
    if features['unique_ratio'] < 0.5:
        suggestions.append("Use more unique characters")
    if strength == 'Strong' and not suggestions:
        suggestions.append("Great password! No suggestions needed.")
    
    return suggestions


# ============================================
# API ENDPOINTS
# ============================================

@app.route('/')
def home():
    return jsonify({"message": "AI Password Analyzer API"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/analyze', methods=['POST'])
def analyze_password():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({"error": "Please provide a password"}), 400
        
        password = data['password']
        
        if not password:
            return jsonify({"error": "Password cannot be empty"}), 400
        
        if model is None:
            return jsonify({"error": "ML model not loaded"}), 500
        
        features = extract_features(password)
        feature_array = np.array([[
            features['length'],
            features['uppercase_count'],
            features['lowercase_count'],
            features['digit_count'],
            features['symbol_count'],
            features['unique_chars'],
            features['unique_ratio'],
            features['repeated_chars']
        ]])
        
        prediction = model.predict(feature_array)[0]
        strength = get_strength_label(prediction)
        risk = get_risk_level(strength)
        score = calculate_score(features, strength)
        suggestions = generate_suggestions(features, strength)
        
        return jsonify({
            "password": password,
            "strength": strength,
            "score": score,
            "risk": risk,
            "suggestions": suggestions,
            "features": features
        })
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# ============================================
# VERCEL HANDLER (REQUIRED)
# ============================================

# DO NOT add app.run() - Vercel handles the server
handler = app