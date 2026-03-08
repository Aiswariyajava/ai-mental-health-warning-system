# ============================================================
# app.py
# AI Mental Health Early Warning System — Streamlit Frontend
# ============================================================

import streamlit as st
import joblib
import time
import os
import re

# ── Page config (must be first Streamlit command) ──────────
st.set_page_config(
    page_title="AI Mental Health Early Warning System",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# SAFETY KEYWORDS — Hard override regardless of model output.
# These phrases are unambiguous crisis signals and must ALWAYS
# map to High risk without relying on ML probabilities.
# ─────────────────────────────────────────────────────────────
CRISIS_KEYWORDS = [
    r"\bwill die\b", r"\bwant to die\b", r"\bwish i was dead\b",
    r"\bkill myself\b", r"\bend my life\b", r"\bend it all\b",
    r"\bhurt myself\b", r"\bsuicide\b", r"\bsuicidal\b",
    r"\bno reason to live\b", r"\bnot worth living\b",
    r"\bfeel like dying\b", r"\bshould just die\b",
    r"\bmight as well be dead\b", r"\bnothing to live for\b",
    r"\bdisappear forever\b", r"\bgoodbye note\b",
    r"\btake my life\b", r"\bdon't want to live\b",
    r"\bwant to end\b", r"\bplanning to die\b",
    r"\bwaste of space\b", r"\bno point being here\b",
    r"\bright to die\b", r"\bready to die\b",
]

def is_crisis_text(text: str) -> bool:
    """Return True if the text contains any explicit crisis keyword."""
    text_lower = text.lower()
    for pattern in CRISIS_KEYWORDS:
        if re.search(pattern, text_lower):
            return True
    return False


# ─────────────────────────────────────────────────────────────
# Custom CSS — Vibrant neon-aurora dark theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background: deep space aurora ── */
.stApp {
    background: linear-gradient(160deg, #05001a 0%, #0d0530 35%, #160a3a 60%, #0a1628 100%);
    min-height: 100vh;
}

/* ── Animated glow orbs ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(139,92,246,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -150px; right: -150px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(236,72,153,0.14) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg,
        rgba(139,92,246,0.45) 0%,
        rgba(236,72,153,0.30) 50%,
        rgba(59,130,246,0.35) 100%);
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 24px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.8rem;
    text-align: center;
    backdrop-filter: blur(16px);
    box-shadow: 0 0 40px rgba(139,92,246,0.25), 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
}
.hero-banner h1 {
    color: #ffffff;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0 0 0.5rem;
    letter-spacing: -0.5px;
    text-shadow: 0 0 30px rgba(167,139,250,0.6);
}
.hero-banner p {
    color: rgba(255,255,255,0.7);
    font-size: 1rem;
    margin: 0;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 18px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ── Textarea ── */
.stTextArea label {
    color: rgba(255,255,255,0.9) !important;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.2px;
}
.stTextArea textarea {
    background: rgba(13,5,48,0.7) !important;
    color: #e2e8f0 !important;
    border: 1.5px solid rgba(139,92,246,0.35) !important;
    border-radius: 14px !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.8) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.2), 0 0 20px rgba(139,92,246,0.15) !important;
}
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.3) !important; }

/* ── Analyse button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #3b82f6 100%) !important;
    background-size: 200% 200% !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.75rem 2rem !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(236,72,153,0.5) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Risk result boxes ── */
.result-box {
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    border: 1.5px solid;
    backdrop-filter: blur(14px);
    position: relative;
    overflow: hidden;
}
.result-box::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
}

/* HIGH — vivid red/orange */
.result-high {
    background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(220,38,38,0.08) 100%);
    border-color: rgba(239,68,68,0.55);
    box-shadow: 0 0 30px rgba(239,68,68,0.2), inset 0 1px 0 rgba(239,68,68,0.15);
}
.result-high::before { background: linear-gradient(90deg, #ef4444, #f97316); }

/* MEDIUM — vivid amber/yellow */
.result-medium {
    background: linear-gradient(135deg, rgba(245,158,11,0.15) 0%, rgba(251,191,36,0.08) 100%);
    border-color: rgba(245,158,11,0.55);
    box-shadow: 0 0 30px rgba(245,158,11,0.2), inset 0 1px 0 rgba(245,158,11,0.15);
}
.result-medium::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

/* LOW — vivid emerald/teal */
.result-low {
    background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(5,150,105,0.08) 100%);
    border-color: rgba(16,185,129,0.55);
    box-shadow: 0 0 30px rgba(16,185,129,0.2), inset 0 1px 0 rgba(16,185,129,0.15);
}
.result-low::before { background: linear-gradient(90deg, #10b981, #06b6d4); }

/* ── Risk badges (pill) ── */
.risk-badge {
    display: inline-block;
    padding: 0.3rem 1.2rem;
    border-radius: 99px;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-left: 0.6rem;
}
.risk-high   { background: rgba(239,68,68,0.2);  color: #fca5a5; border: 1.5px solid rgba(239,68,68,0.6); }
.risk-medium { background: rgba(245,158,11,0.2); color: #fde68a; border: 1.5px solid rgba(245,158,11,0.6); }
.risk-low    { background: rgba(16,185,129,0.2); color: #6ee7b7; border: 1.5px solid rgba(16,185,129,0.6); }

/* ── Suggestions ── */
.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.6rem 0;
    color: rgba(255,255,255,0.85);
    font-size: 0.94rem;
    line-height: 1.5;
    border-bottom: 1px solid rgba(139,92,246,0.12);
}
.suggestion-item:last-child { border-bottom: none; }
.suggestion-icon { font-size: 1.15rem; flex-shrink: 0; margin-top: 1px; }

/* ── Metric tiles ── */
.metric-row {
    display: flex;
    gap: 0.9rem;
    margin: 0.3rem 0 1.5rem;
}
.metric-tile {
    flex: 1;
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(59,130,246,0.08));
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-tile:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(139,92,246,0.2);
}
.metric-tile .val {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-tile .lbl {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.45);
    margin-top: 3px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Confidence label ── */
.conf-label {
    color: rgba(255,255,255,0.6);
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
}
.conf-label b { color: rgba(255,255,255,0.9); }

/* ── Progress bar colour fix (Streamlit default is red-ish) ── */
.stProgress > div > div { border-radius: 99px !important; }

/* ── Emergency banner ── */
.emergency-banner {
    background: linear-gradient(135deg, rgba(239,68,68,0.25), rgba(220,38,38,0.15));
    border: 2px solid rgba(239,68,68,0.7);
    border-radius: 16px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1rem;
    animation: pulse-border 2s infinite;
}
@keyframes pulse-border {
    0%,100% { box-shadow: 0 0 10px rgba(239,68,68,0.3); }
    50%      { box-shadow: 0 0 25px rgba(239,68,68,0.6); }
}
.emergency-banner h3 { color: #fca5a5; margin: 0 0 0.4rem; font-size: 1.1rem; }
.emergency-banner p  { color: rgba(255,255,255,0.85); margin: 0; font-size: 0.93rem; line-height: 1.6; }

/* ── Disclaimer ── */
.disclaimer {
    background: rgba(139,92,246,0.08);
    border-left: 3px solid rgba(139,92,246,0.6);
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    color: rgba(255,255,255,0.5);
    font-size: 0.82rem;
    margin-top: 1.2rem;
    line-height: 1.5;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(5,0,26,0.97), rgba(13,5,48,0.95)) !important;
    border-right: 1px solid rgba(139,92,246,0.2);
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 { color: #a78bfa !important; }

/* ── Footer ── */
.footer-txt {
    text-align: center;
    color: rgba(255,255,255,0.2);
    font-size: 0.8rem;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(139,92,246,0.1);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Auto-train helper — runs only if pkl files are missing.
# This makes the app self-contained on Streamlit Cloud where
# you cannot run train_model.py separately before deployment.
# ─────────────────────────────────────────────────────────────
def _train_and_save():
    """Train model from dataset.csv and save to model/ folder."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    df = pd.read_csv("dataset.csv")
    X, y = df["text"], df["label"]
    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    vec = TfidfVectorizer(
        max_features=5000, stop_words="english",
        ngram_range=(1, 2), sublinear_tf=True
    )
    X_vec = vec.fit_transform(X_train)
    clf = LogisticRegression(max_iter=1000, solver="lbfgs", C=1.0, random_state=42)
    clf.fit(X_vec, y_train)

    os.makedirs("model", exist_ok=True)
    joblib.dump(clf, os.path.join("model", "mental_health_model.pkl"))
    joblib.dump(vec, os.path.join("model", "tfidf_vectorizer.pkl"))
    return clf, vec


# ─────────────────────────────────────────────────────────────
# Load model & vectorizer (cached for performance).
# Auto-trains if pkl files are not found.
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    """
    Load the trained ML model and TF-IDF vectorizer.
    If model files do not exist (e.g. first run on Streamlit Cloud),
    they are trained automatically from dataset.csv.
    """
    model_path = os.path.join("model", "mental_health_model.pkl")
    vec_path   = os.path.join("model", "tfidf_vectorizer.pkl")

    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        # ── First-run: train + save, then return ──────────────
        return _train_and_save()

    return joblib.load(model_path), joblib.load(vec_path)


# ─────────────────────────────────────────────────────────────
# Predict risk level (with crisis keyword override)
# ─────────────────────────────────────────────────────────────
def predict_risk(text: str, model, vectorizer) -> dict:
    """
    Predict mental health risk for the given text.
    Safety Override: If explicit crisis keywords are detected, the
    result is immediately forced to 'High' regardless of model output.
    """
    # ── Safety override (runs FIRST, before ML) ──────────────
    if is_crisis_text(text):
        classes = model.classes_.tolist()
        probs = {cls: 0.03 for cls in classes}
        probs["High"] = 0.94
        return {"label": "High", "probabilities": probs, "override": True}

    # ── Normal ML prediction ──────────────────────────────────
    text_vec   = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    proba      = model.predict_proba(text_vec)[0]
    classes    = model.classes_

    prob_dict = {cls: float(p) for cls, p in zip(classes, proba)}
    return {"label": prediction, "probabilities": prob_dict, "override": False}


# ─────────────────────────────────────────────────────────────
# Suggestions content per risk level
# ─────────────────────────────────────────────────────────────
SUGGESTIONS = {
    "High": {
        "emoji": "🚨",
        "color_class": "result-high",
        "badge_class": "risk-high",
        "headline": "High Risk — You Are Not Alone. Help Is Here.",
        "intro": (
            "Your message suggests you may be in severe emotional distress or crisis. "
            "Please reach out for support immediately — you deserve care and you matter."
        ),
        "items": [
            ("📞", "Call a crisis helpline NOW — iCall: 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7, free)"),
            ("🏥", "Go to your nearest emergency room or mental health clinic if you feel unsafe."),
            ("💬", "Tell someone you trust exactly how you're feeling right now — don't face this alone."),
            ("🛑", "If you feel an immediate urge to harm yourself, call emergency services (112) immediately."),
            ("📵", "Step away from anything that increases your distress — social media, news, etc."),
            ("🌬️", "Try box breathing to ground yourself: inhale 4s → hold 4s → exhale 6s → repeat."),
            ("📝", "Name 5 things you can see, 4 you can touch, 3 you can hear — it helps anchor you."),
        ],
    },
    "Medium": {
        "emoji": "⚠️",
        "color_class": "result-medium",
        "badge_class": "risk-medium",
        "headline": "Medium Risk — Let's Work Through This Together",
        "intro": (
            "You appear to be going through a difficult period. It's completely okay to feel this way. "
            "Small, consistent actions can create meaningful change."
        ),
        "items": [
            ("🧘", "Practice 10 minutes of mindfulness or meditation daily — try Calm or Headspace."),
            ("🚶", "Take a 20–30 minute walk outdoors — movement powerfully resets your nervous system."),
            ("🗣️", "Open up to someone you trust about what you're going through — sharing lightens the load."),
            ("📅", "Consider scheduling a session with a licensed therapist or counselor this week."),
            ("😴", "Prioritise 7–8 hours of sleep and stick to a consistent bedtime each night."),
            ("📓", "Keep a brief daily mood journal to spot patterns and identify your stress triggers."),
            ("🥗", "Nourish your body — balanced meals, stay hydrated, and reduce caffeine intake."),
        ],
    },
    "Low": {
        "emoji": "✅",
        "color_class": "result-low",
        "badge_class": "risk-low",
        "headline": "Low Risk — You're Doing Great! Keep It Up.",
        "intro": (
            "You appear to be in a healthy, positive mental state. "
            "Maintaining these habits now builds resilience for harder times ahead."
        ),
        "items": [
            ("🏋️", "Keep up regular physical activity — even a 20-minute walk boosts mood and focus."),
            ("🙏", "Practice daily gratitude — write 3 things you're thankful for each morning."),
            ("🤝", "Nurture your social connections; invest time in people who energise you."),
            ("📚", "Engage in mentally stimulating activities that spark creativity and curiosity."),
            ("🌙", "Protect your sleep hygiene — quality rest is the foundation of mental wellbeing."),
            ("💧", "Stay hydrated and eat mindfully throughout the day."),
            ("🧠", "Learn a stress-management technique (e.g., box breathing) as a preventive tool."),
        ],
    },
}


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 About This Tool")
    st.markdown(
        "This AI-powered system uses **Natural Language Processing (NLP)** "
        "and **Machine Learning** to assess the emotional tone of your message "
        "and provide a mental health risk estimate."
    )
    st.markdown("---")
    st.markdown("### 🔬 How It Works")
    st.markdown(
        "1. **Crisis Override** — Explicit danger phrases are caught instantly.\n"
        "2. **TF-IDF** converts your text into numerical features.\n"
        "3. **Logistic Regression** classifies the risk level.\n"
        "4. **Tailored suggestions** are shown based on the result."
    )
    st.markdown("---")
    st.markdown("### 📞 Crisis Resources (India)")
    st.markdown(
        "- **iCall**: 9152987821\n"
        "- **Vandrevala Foundation**: 1860-2662-345\n"
        "- **Snehi**: 044-24640050\n"
        "- **iCall (Online)**: icallhelpline.org\n"
        "- **Emergency**: 112"
    )
    st.markdown("---")
    st.markdown(
        "<div style='color:rgba(255,255,255,0.3);font-size:0.78rem;'>"
        "Built with Python · scikit-learn · Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# Main UI
# ─────────────────────────────────────────────────────────────

# Hero banner
st.markdown("""
<div class="hero-banner">
    <h1>🧠 AI Mental Health Early Warning System</h1>
    <p>Share how you're feeling. Our AI will assess your emotional state and offer personalised support.</p>
</div>
""", unsafe_allow_html=True)

# Metric tiles
st.markdown("""
<div class="metric-row">
    <div class="metric-tile"><div class="val">3</div><div class="lbl">Risk Levels</div></div>
    <div class="metric-tile"><div class="val">NLP</div><div class="lbl">TF-IDF Engine</div></div>
    <div class="metric-tile"><div class="val">ML</div><div class="lbl">Logistic Reg.</div></div>
    <div class="metric-tile"><div class="val">24/7</div><div class="lbl">Always On</div></div>
</div>
""", unsafe_allow_html=True)

# Load model (auto-trains on first run if needed)
if not os.path.exists(os.path.join("model", "mental_health_model.pkl")):
    with st.spinner("⚙️ Setting up model for the first time — this takes ~5 seconds..."):
        model, vectorizer = load_artifacts()
else:
    model, vectorizer = load_artifacts()

# Input section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 💬 How are you feeling today?")

user_input = st.text_area(
    label="Describe your thoughts, feelings, or recent experiences in your own words:",
    placeholder=(
        "e.g. 'I've been feeling overwhelmed lately and can't seem to relax. "
        "My sleep has been poor and I find it hard to enjoy things...'"
    ),
    height=165,
    key="user_input_area",
)

analyze_btn = st.button("🔍  Analyse My Mental State", key="analyze_btn")
st.markdown("</div>", unsafe_allow_html=True)

# ── Prediction and Results ────────────────────────────────────
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️  Please enter some text before clicking Analyse.")
    elif len(user_input.strip().split()) < 2:
        st.warning("⚠️  Please provide a bit more detail for an accurate assessment.")
    else:
        with st.spinner("🧠 Analysing your message..."):
            time.sleep(1.0)
            result = predict_risk(user_input.strip(), model, vectorizer)

        label    = result["label"]
        probs    = result["probabilities"]
        conf     = probs[label] * 100
        override = result["override"]
        info     = SUGGESTIONS[label]

        # ── Emergency banner for crisis override ─────────────
        if override:
            st.markdown("""
            <div class="emergency-banner">
                <h3>🚨 Crisis Alert — Immediate Support Available</h3>
                <p>
                    Your message contains language that signals you may be in serious danger.
                    Please contact a crisis helpline or emergency services <strong>right now</strong>.<br>
                    <strong>iCall:</strong> 9152987821 &nbsp;|&nbsp;
                    <strong>Vandrevala (24/7):</strong> 1860-2662-345 &nbsp;|&nbsp;
                    <strong>Emergency:</strong> 112
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ── Risk result box ───────────────────────────────────
        st.markdown(
            f"<div class='result-box {info['color_class']}'>"
            f"  <h2 style='color:white;margin:0 0 0.5rem;font-size:1.4rem;font-weight:700;'>"
            f"  {info['emoji']} &nbsp;{info['headline']}"
            f"  </h2>"
            f"  <p style='color:rgba(255,255,255,0.78);margin:0;font-size:0.96rem;line-height:1.6;'>"
            f"  {info['intro']}"
            f"  </p>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── Risk badge + confidence ───────────────────────────
        st.markdown(
            f"**Detected Risk Level:** "
            f"<span class='risk-badge {info['badge_class']}'>{label}</span>",
            unsafe_allow_html=True,
        )

        if not override:
            st.markdown(
                f"<div class='conf-label'>Model Confidence: <b>{conf:.1f}%</b></div>",
                unsafe_allow_html=True,
            )
            st.progress(int(conf))
        else:
            st.markdown(
                "<div class='conf-label'>Detection: <b>Crisis keyword override active</b> — "
                "Immediate escalation to High Risk.</div>",
                unsafe_allow_html=True,
            )
            st.progress(100)

        # ── Probability breakdown (expandable) ───────────────
        if not override:
            with st.expander("📊 View full probability breakdown"):
                cols = st.columns(3)
                for i, cls in enumerate(["High", "Medium", "Low"]):
                    p = probs.get(cls, 0) * 100
                    cols[i].metric(label=f"{cls} Risk", value=f"{p:.1f}%")

        # ── Personalised suggestions ─────────────────────────
        st.markdown("### 💡 Personalised Suggestions")
        html = ""
        for icon, text in info["items"]:
            html += (
                f"<div class='suggestion-item'>"
                f"  <span class='suggestion-icon'>{icon}</span>"
                f"  <span>{text}</span>"
                f"</div>"
            )
        st.markdown(f"<div class='glass-card'>{html}</div>", unsafe_allow_html=True)

        # ── Disclaimer ────────────────────────────────────────
        st.markdown(
            "<div class='disclaimer'>"
            "⚠️ <b>Disclaimer:</b> This tool is for informational and educational purposes only. "
            "It is <b>not</b> a substitute for professional medical or psychiatric advice, diagnosis, "
            "or treatment. If you are in crisis, please contact a mental health professional or "
            "emergency services immediately. &nbsp;| &nbsp;"
            "<b>iCall:</b> 9152987821 &nbsp;| &nbsp;<b>Emergency:</b> 112"
            "</div>",
            unsafe_allow_html=True,
        )

# Footer
if not analyze_btn:
    st.markdown(
        "<div class='footer-txt'>"
        "🔒 Your text is processed locally and is never stored or transmitted."
        "</div>",
        unsafe_allow_html=True,
    )
