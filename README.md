# 🧠 AI Mental Health Early Warning System

An intermediate-level Machine Learning project that analyses free-form text input
and predicts a **mental health risk level** (Low / Medium / High), then provides
tailored supportive suggestions — all through a beautiful Streamlit web interface.

---

## 📁 Project Structure

```
p1/
├── dataset.csv          # Labelled training data (text + risk label)
├── train_model.py       # Training pipeline: TF-IDF + Logistic Regression
├── app.py               # Streamlit web application
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── model/               # Auto-created after training
    ├── mental_health_model.pkl
    └── tfidf_vectorizer.pkl
```

---

## 🛠️ Setup Instructions

### 1 — Prerequisites
Make sure Python 3.9+ is installed. Verify with:
```bash
python --version
```

### 2 — Install Dependencies
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3 — Train the Model
```bash
python train_model.py
```
This will:
- Load `dataset.csv`
- Vectorize text with **TF-IDF**
- Train a **Logistic Regression** classifier
- Print accuracy and classification report
- Save the model to `model/mental_health_model.pkl`
- Save the vectorizer to `model/tfidf_vectorizer.pkl`

### 4 — Launch the Web App
```bash
streamlit run app.py
```
Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

---

## 🔬 How It Works

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **Dataset** | 100 labelled text samples across Low / Medium / High risk |
| 2 | **TF-IDF** | Converts text into numerical feature vectors (top 5000 n-grams) |
| 3 | **Logistic Regression** | Multi-class classifier trained on the vectors |
| 4 | **Prediction** | Outputs risk label + confidence scores |
| 5 | **Suggestions** | Curated support messages served per risk level |

---

## 🎯 Risk Levels

| Level | Meaning | Example Signal |
|-------|---------|---------------|
| 🔴 **High** | Severe distress / crisis indicators | "I feel like I can't go on" |
| 🟡 **Medium** | Moderate stress / low mood | "I've been anxious and sleeping poorly" |
| 🟢 **Low** | Generally positive / stable | "Feeling great and motivated today" |

---

## 📞 Crisis Helplines (India)
- **iCall**: 9152987821
- **Vandrevala Foundation**: 1860-2662-345 (24/7)
- **Snehi**: 044-24640050
- **Emergency**: 112

---

## ⚠️ Disclaimer
This tool is for **educational and informational purposes only**.
It is **not** a medical device and does not replace professional psychiatric assessment or treatment.
