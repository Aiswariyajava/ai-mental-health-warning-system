# 🚀 Deployment Guide — Streamlit Cloud

## Step 1: Push to GitHub

If you haven't already, initialize a Git repository and push your code:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Mental Health Early Warning System with History"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/mental-health-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Sign in** with GitHub (create account if needed)

3. **Click "New app"** button

4. **Fill in the deployment form:**
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain

5. **Click "Deploy"** and wait ~2-3 minutes

## Step 3: Configure on Streamlit Cloud

Once deployed, go to **App menu → Settings → Advanced settings** and add:

```toml
[theme]
primaryColor = "#7c3aed"
backgroundColor = "#05001a"
secondaryBackgroundColor = "#0d0530"
textColor = "#ffffff"

[server]
enableXsrfProtection = true
enableCORS = false
maxUploadSize = 200
```

## What Gets Stored

- **SQLite Database**: The `analysis_history.db` will be stored in Streamlit Cloud's file system
- **Model Files**: `model/mental_health_model.pkl` and `model/tfidf_vectorizer.pkl` are auto-trained on first run

## Important Notes

⚠️ **Data Persistence**: 
- Streamlit Cloud stores files in a temporary filesystem
- Your `analysis_history.db` will reset when the app restarts
- For permanent storage, consider integrating a cloud database (PostgreSQL, MongoDB, etc.)

✅ **Features Included**:
- Real-time risk assessment
- Crisis keyword detection
- Personalized suggestions
- Full analysis history
- Dark theme with aurora effect

## Troubleshooting

**App won't load?**
- Check that all dependencies in `requirements.txt` are installed
- Verify `app.py` syntax: `python -m py_compile app.py`

**History not persisting?**
- This is expected on Streamlit Cloud (file system resets)
- Use the local version for persistent history

**Need to update the app?**
- Simply push new changes to GitHub
- Streamlit Cloud will auto-redeploy in ~1 minute

---

**Live URL**: `https://YOUR-USERNAME-mental-health-ai.streamlit.app`
