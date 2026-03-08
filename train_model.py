# ============================================================
# train_model.py
# AI Mental Health Early Warning System
# ============================================================
# This script:
#   1. Loads the labeled text dataset (dataset.csv)
#   2. Vectorizes text using TF-IDF
#   3. Trains a Logistic Regression classifier
#   4. Evaluates the model with accuracy & classification report
#   5. Saves the trained model and vectorizer using joblib
# ============================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ─────────────────────────────────────────────
# Step 1: Load the dataset
# ─────────────────────────────────────────────
print("📂 Loading dataset...")

df = pd.read_csv("dataset.csv")

# Show basic info about the loaded data
print(f"✅ Loaded {len(df)} samples")
print(f"   Label distribution:\n{df['label'].value_counts()}\n")

# ─────────────────────────────────────────────
# Step 2: Prepare features (X) and labels (y)
# ─────────────────────────────────────────────
X = df["text"]       # Input text (user messages)
y = df["label"]      # Target label: Low / Medium / High

# ─────────────────────────────────────────────
# Step 3: Split into training and test sets
# ─────────────────────────────────────────────
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📊 Training samples: {len(X_train)} | Test samples: {len(X_test)}\n")

# ─────────────────────────────────────────────
# Step 4: Vectorize text using TF-IDF
# ─────────────────────────────────────────────
# TF-IDF converts raw text into numerical feature vectors.
# max_features=5000 means we keep only the top 5000 words by frequency.
# ngram_range=(1, 2) captures both single words and two-word phrases.
print("🔤 Vectorizing text with TF-IDF...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english",    # Remove common English stop words
    ngram_range=(1, 2),      # Use unigrams and bigrams
    sublinear_tf=True        # Apply log normalization to term frequency
)

# Fit the vectorizer on training data and transform both sets
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

print(f"✅ Vocabulary size: {len(vectorizer.vocabulary_)}\n")

# ─────────────────────────────────────────────
# Step 5: Train Logistic Regression model
# ─────────────────────────────────────────────
# Logistic Regression is effective for text classification tasks.
# 'max_iter=1000' ensures convergence on this dataset.
print("🧠 Training Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs",   # Efficient solver; handles multi-class natively in sklearn >= 1.5
    C=1.0,            # Regularization strength (1.0 = balanced)
    random_state=42
)

model.fit(X_train_vec, y_train)
print("✅ Model training complete!\n")

# ─────────────────────────────────────────────
# Step 6: Evaluate the model
# ─────────────────────────────────────────────
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
print(f"📈 Test Accuracy: {accuracy * 100:.2f}%\n")
print("📋 Classification Report:")
print(classification_report(y_test, y_pred))

# ─────────────────────────────────────────────
# Step 7: Save the model and vectorizer to disk
# ─────────────────────────────────────────────
# We use joblib for efficient serialization of sklearn objects.
os.makedirs("model", exist_ok=True)

joblib.dump(model,      "model/mental_health_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("💾 Model saved  →  model/mental_health_model.pkl")
print("💾 Vectorizer saved  →  model/tfidf_vectorizer.pkl")
print("\n✅ Training pipeline complete! You can now run 'streamlit run app.py'")
