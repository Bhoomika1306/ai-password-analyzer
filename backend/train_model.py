# ============================================
# train_model.py - ML Model Training
# ============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import re


# ============================================
# STEP 1: CREATE TRAINING DATASET
# ============================================

def create_dataset():
    """
    Creates a dataset of passwords with their strength labels.
    Labels: 0 = Weak, 1 = Medium, 2 = Strong
    """
    
    # WEAK PASSWORDS (Label: 0) - Simple, common, short
    weak_passwords = [
        '123456', 'password', 'qwerty', 'abc123', 'letmein',
        'welcome', 'monkey', 'dragon', 'master', 'sunshine',
        'princess', 'admin', 'login', 'football', 'baseball',
        'iloveyou', 'trustno1', '696969', 'batman', 'passw0rd',
        'hello', 'password1', '123456789', 'qwerty123', 'admin123',
        'welcome1', 'monkey1', 'dragon1', 'sunshine1', 'princess1',
        'abc', 'xyz', 'cat', 'dog', 'red', 'blue', 'green', 'test',
        'user', 'guest', 'default', 'temp', 'new', 'old', 'first',
        'a', 'ab', '12', '123', 'qwe', 'asd', 'zxc', 'password123',
        'qwertyuiop', 'asdfghjkl', '111111', '222222', '333333',
    ]
    
    # MEDIUM PASSWORDS (Label: 1) - Some complexity but predictable
    medium_passwords = [
        'Hello1', 'Welcome2', 'Dragon3', 'Monkey4', 'Sunshine5',
        'Password1', 'Qwerty2', 'Abcdef3', 'Letmein4', 'Master5',
        'Football1', 'Baseball2', 'Princess3', 'Sunshine4', 'Dragon5',
        'Hello123', 'Welcome456', 'Test789', 'User1234', 'Guest5678',
        'Apple1', 'Banana2', 'Cherry3', 'Orange4', 'Grape5',
        'House1', 'Car2', 'Tree3', 'Book4', 'Phone5',
        'Summer1', 'Winter2', 'Spring3', 'Autumn4', 'Rain5',
        'Music1', 'Movie2', 'Game3', 'Sport4', 'Food5',
        'BlueSky1', 'RedCar2', 'GreenTree3', 'HappyDay4', 'NiceTime5',
        'Strong1', 'Power2', 'Light3', 'Water4', 'Fire5',
        'Mountain1', 'River2', 'Ocean3', 'Forest4', 'Desert5',
        'Eagle1', 'Tiger2', 'Lion3', 'Wolf4', 'Bear5',
        'Coffee1', 'Pizza2', 'Burger3', 'Pasta4', 'Salad5',
        'School1', 'College2', 'University3', 'Student4', 'Teacher5',
        'Doctor1', 'Nurse2', 'Police3', 'Fireman4', 'Soldier5',
        'America1', 'England2', 'France3', 'Germany4', 'Japan5',
        'Monday1', 'Tuesday2', 'Wednesday3', 'Thursday4', 'Friday5',
    ]
    
    # STRONG PASSWORDS (Label: 2) - Complex, mixed characters
    strong_passwords = [
        'Hello@123', 'Welcome#456', 'Dragon$789', 'Monkey%101', 'Sunshine&202',
        'Password!1', 'Qwerty@2', 'Abcdef#3', 'Letmein$4', 'Master%5',
        'Football!1', 'Baseball@2', 'Princess#3', 'Sunshine$4', 'Dragon%5',
        'Hello123!', 'Welcome456@', 'Test789#', 'User1234$', 'Guest5678%',
        'Apple!1B2', 'Banana@2C3', 'Cherry#3D4', 'Orange$4E5', 'Grape%5F6',
        'House!1A2', 'Car@2B3', 'Tree#3C4', 'Book$4D5', 'Phone%5E6',
        'Summer!1Day', 'Winter@2Night', 'Spring#3Morning', 'Autumn$4Evening', 'Rain%5Storm',
        'Music!1Lover', 'Movie@2Fan', 'Game#3Player', 'Sport$4Star', 'Food%5Chef',
        'BlueSky!1', 'RedCar@2', 'GreenTree#3', 'HappyDay$4', 'NiceTime%5',
        'Strong!1Pass', 'Power@2User', 'Light#3Beam', 'Water$4Flow', 'Fire%5Blaze',
        'Mountain!1High', 'River@2Deep', 'Ocean#3Wide', 'Forest$4Dark', 'Desert%5Hot',
        'Eagle!1Fly', 'Tiger@2Run', 'Lion#3Roar', 'Wolf$4Howl', 'Bear%5Growl',
        'Coffee!1Mug', 'Pizza@2Slice', 'Burger#3Bite', 'Pasta$4Plate', 'Salad%5Bowl',
        'School!1Learn', 'College@2Study', 'University#3Degree', 'Student$4Life', 'Teacher%5Work',
        'Doctor!1Heal', 'Nurse@2Care', 'Police#3Law', 'Fireman$4Save', 'Soldier%5Fight',
        'America!1USA', 'England@2UK', 'France#3EU', 'Germany$4DE', 'Japan%5JP',
        'Monday!1Start', 'Tuesday@2Work', 'Wednesday#3Mid', 'Thursday$4Late', 'Friday%5End',
        'Xk9#mP2$vL5', 'Qw!3Rt@5Yz', 'Ab#1Cd$3Ef', 'Gh!5Ij@7Kl', 'Mn#9Op$1Qr',
        'St!2Uv@4Wx', 'Yz#6Ab$8Cd', 'Ef!0Gh@2Ij', 'Kl#4Mn$6Op', 'Qr!8St@0Uv',
        'Wx#2Yz$4Ab', 'Cd!6Ef@8Gh', 'Ij#0Kl$2Mn', 'Op!4Qr@6St', 'Uv#8Wx$0Yz',
        'MyP@ssw0rd!2024', 'S3cur3#N0w$', 'Str0ng!P@ss1', 'Pr0t3ct#M3@', 'Saf3&N0w!2024',
        'C0mpl3x#P@ss$', 'Un1qu3!Str0ng@', 'P0w3r#S3cur3$', 'D3f3nd!Mys3lf@', 'Gu@rd1an#2024$',
        'N3v3r!G1v3Up@', 'Alw@ys#Str0ng$', 'B3st!P@ssw0rd@', 'Ult1m@t3#S3c$', 'M@st3r!K3y2024#',
        'Sup3r!S3cur3@', 'M3g@#Str0ng$', 'Hyp3r!S@f3@', 'Ultr@#P0w3r$', 'Extr3m3!S3c@',
        'T0t@l#S@f3ty$', 'Abs0lut3!S3cur3@', 'P3rf3ct#P@ss$', '1d3@l!S@f3@', 'Supr3m3#Str0ng$',
        'Tru3!S3cur1ty@', 'R3@l#P0w3r$', 'Pur3!S@f3@', 'Cl3@n#Str0ng$', 'S1mpl3!S3cur3@',
        'Sm@rt#P@ss$', 'Br1ll1@nt!S@f3@', 'Aw3s0m3#Str0ng$', 'F@nt@st1c!S3c@', 'W0nd3rful#P@ss$',
        'Am@z1ng!S3cur3@', 'Exc3ll3nt#Str0ng$', 'Gr3@t!S@f3@', 'Sup3rb#P@ss$', '0utst@nd1ng!S3c@',
    ]
    
    # Combine all passwords
    all_passwords = weak_passwords + medium_passwords + strong_passwords
    
    # Create labels (0 for weak, 1 for medium, 2 for strong)
    all_labels = (
        [0] * len(weak_passwords) +
        [1] * len(medium_passwords) +
        [2] * len(strong_passwords)
    )
    
    # Verify they match
    assert len(all_passwords) == len(all_labels), f"Mismatch: {len(all_passwords)} passwords vs {len(all_labels)} labels"
    
    # Create DataFrame
    df = pd.DataFrame({
        'password': all_passwords,
        'strength': all_labels
    })
    
    print(f"✅ Dataset created with {len(df)} passwords!")
    print(f"   - Weak passwords: {len(df[df['strength'] == 0])}")
    print(f"   - Medium passwords: {len(df[df['strength'] == 1])}")
    print(f"   - Strong passwords: {len(df[df['strength'] == 2])}")
    
    return df


# ============================================
# STEP 2: EXTRACT FEATURES FROM PASSWORDS
# ============================================

def extract_features(password):
    """
    Convert a password into numerical features that the ML model can understand.
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


def prepare_features(df):
    """
    Apply feature extraction to all passwords in our dataset.
    """
    print("\n🔍 Extracting features from passwords...")
    
    feature_list = df['password'].apply(extract_features)
    X = pd.DataFrame(feature_list.tolist())
    y = df['strength']
    
    print(f"✅ Features extracted! Each password now has {X.shape[1]} features.")
    print(f"   Feature names: {list(X.columns)}")
    
    return X, y


# ============================================
# STEP 3: TRAIN THE MODEL
# ============================================

def train_model(X, y):
    """
    Train a Random Forest classifier to predict password strength.
    """
    
    print("\n🤖 Training the Machine Learning model...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n🎯 Model Training Complete!")
    print(f"   Accuracy: {accuracy * 100:.2f}%")
    print(f"\n📊 Detailed Report:")
    print(classification_report(y_test, y_pred, target_names=['Weak', 'Medium', 'Strong']))
    
    return model


# ============================================
# STEP 4: SAVE THE MODEL
# ============================================

def save_model(model, filename='model.pkl'):
    """
    Save the trained model to a file using pickle.
    """
    
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    
    print(f"\n💾 Model saved as '{filename}'")
    print("   You can now use this file in your Flask app!")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("🔐 AI Password Strength Analyzer - ML Training")
    print("=" * 50)
    
    df = create_dataset()
    X, y = prepare_features(df)
    model = train_model(X, y)
    save_model(model)
    
    print("\n" + "=" * 50)
    print("🎉 Training Complete! Ready for predictions.")
    print("=" * 50)