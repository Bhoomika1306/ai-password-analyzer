# ============================================
# app.py - Flask API with ML Prediction
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

# Create Flask app
app = Flask(__name__)

# Allow requests from your Vercel frontend and local development
CORS(app, origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "https://ai-password-analyzer-iqnuggvwy-bhoomika1306-projects.vercel.app"
])


# ============================================
# LOAD THE TRAINED MODEL
# ============================================

# Load the model we trained in train_model.py
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

print("✅ ML Model loaded successfully!")


# ============================================
# FEATURE EXTRACTION (same as train_model.py)
# ============================================

def extract_features(password):
    """
    Convert password into numerical features.
    MUST match exactly what we used during training!
    """
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
    """Convert numeric prediction to text label."""
    labels = {0: 'Weak', 1: 'Medium', 2: 'Strong'}
    return labels.get(prediction, 'Unknown')


def get_risk_level(strength):
    """Determine risk based on strength."""
    risk_map = {
        'Weak': 'High',
        'Medium': 'Medium',
        'Strong': 'Low'
    }
    return risk_map.get(strength, 'Unknown')


def calculate_score(features, strength):
    """
    Calculate a score from 0-100 based on password features.
    """
    score = 0
    
    # Length scoring (max 30 points)
    length = features['length']
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 10
    else:
        score += 5
    
    # Character variety scoring (max 40 points)
    if features['uppercase_count'] > 0:
        score += 10
    if features['lowercase_count'] > 0:
        score += 10
    if features['digit_count'] > 0:
        score += 10
    if features['symbol_count'] > 0:
        score += 10
    
    # Uniqueness scoring (max 20 points)
    if features['unique_ratio'] > 0.8:
        score += 20
    elif features['unique_ratio'] > 0.6:
        score += 15
    elif features['unique_ratio'] > 0.4:
        score += 10
    else:
        score += 5
    
    # No repeated characters bonus (max 10 points)
    if features['repeated_chars'] == 0:
        score += 10
    elif features['repeated_chars'] <= 2:
        score += 5
    
    # Adjust based on ML prediction
    if strength == 'Weak':
        score = min(score, 40)
    elif strength == 'Medium':
        score = min(max(score, 41), 70)
    else:
        score = max(score, 71)
    
    return min(score, 100)


def generate_suggestions(features, strength):
    """
    Generate smart suggestions to improve the password.
    """
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
        suggestions.append("Avoid repeating characters (e.g., 'aaa', '111')")
    
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
    """Home page - check if server is running."""
    return "🔐 AI Password Strength Analyzer Backend is Running!"


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Backend is up and running!"
    })


@app.route('/analyze', methods=['POST'])
def analyze_password():
    """
    MAIN API ENDPOINT
    
    Receives: {"password": "your_password_here"}
    Returns: {
        "strength": "Strong",
        "score": 92,
        "risk": "Low",
        "suggestions": ["..."]
    }
    """
    try:
        # Get password from request body
        data = request.get_json()
        
        # Validate input
        if not data or 'password' not in data:
            return jsonify({
                "error": "Please provide a password in the request body"
            }), 400
        
        password = data['password']
        
        # Handle empty password
        if not password:
            return jsonify({
                "error": "Password cannot be empty"
            }), 400
        
        # Extract features from the password
        features = extract_features(password)
        
        # Convert features to array format for the model
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
        
        # Make prediction using our trained model
        prediction = model.predict(feature_array)[0]
        
        # Convert prediction to readable format
        strength = get_strength_label(prediction)
        risk = get_risk_level(strength)
        score = calculate_score(features, strength)
        suggestions = generate_suggestions(features, strength)
        
        # Return the result
        return jsonify({
            "password": password,
            "strength": strength,
            "score": score,
            "risk": risk,
            "suggestions": suggestions,
            "features": features
        })
    
    except Exception as e:
        # If something goes wrong, return error message
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Use PORT from environment variable (for Render), default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # At the bottom of backend/app.py
handler = app