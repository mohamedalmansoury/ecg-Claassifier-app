# Streamlit Community Cloud Deployment Guide

## Prerequisites
1. GitHub account
2. Git installed on your system
3. Streamlit Community Cloud account (free at https://share.streamlit.io/)

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website
1. Go to https://github.com/new
2. Repository name: `ecg-classifier-app`
3. Description: "ECG Classification with Parallel xLSTM"
4. Choose Public or Private
5. DO NOT initialize with README (we'll push existing code)
6. Click "Create repository"

### Option B: Using GitHub CLI (if installed)
```bash
gh repo create ecg-classifier-app --public --source=. --remote=origin
```

## Step 2: Initialize Git and Push Code

Run these commands in PowerShell from the deployment folder:

```powershell
# Navigate to deployment folder
cd "c:\Users\Al Mansoury\Downloads\results (1)\deployment"

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: ECG classifier with xLSTM"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ecg-classifier-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Prepare for Deployment

### Important Files Needed:
1. ✅ `app.py` - Main application
2. ✅ `model_inference.py` - Model loading
3. ✅ `utils.py` - Preprocessing utilities
4. ✅ `requirements.txt` - Dependencies
5. ⚠️ Model files (see below)

### Model Files Issue
Your model checkpoint is too large for GitHub (>100MB limit).

**Solutions:**

#### Option 1: Git LFS (Recommended)
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.ckpt"
git lfs track "*.npz"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"

# Add and push large files
git add xlstm_100hz_parallel_final.ckpt normalization_params.npz
git commit -m "Add model files"
git push
```

#### Option 2: External Storage (Alternative)
Use Google Drive, Dropbox, or Hugging Face Hub:

1. Upload files to cloud storage
2. Get direct download link
3. Modify `app.py` to download on startup:

```python
import requests
import os

def download_model():
    if not os.path.exists('xlstm_100hz_parallel_final.ckpt'):
        url = 'YOUR_DIRECT_DOWNLOAD_LINK'
        with st.spinner('Downloading model...'):
            response = requests.get(url)
            with open('xlstm_100hz_parallel_final.ckpt', 'wb') as f:
                f.write(response.content)

# Call at startup
download_model()
```

## Step 4: Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account
4. Select:
   - Repository: `YOUR_USERNAME/ecg-classifier-app`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

## Step 5: Configure Secrets (if needed)

If you use external storage, add secrets in Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Add:
```toml
MODEL_URL = "your_model_download_url"
NORM_PARAMS_URL = "your_params_download_url"
```

## Step 6: Monitor Deployment

Watch the deployment logs for:
- ✅ Dependencies installation
- ✅ Model loading
- ✅ App startup
- ⚠️ Any errors

## Common Issues & Solutions

### Issue: "Module not found"
**Solution**: Update `requirements.txt` with exact versions

### Issue: "Memory error"
**Solution**: Streamlit free tier has 1GB RAM limit
- Optimize model loading
- Use CPU-only PyTorch
- Consider caching with `@st.cache_resource`

### Issue: "Timeout during startup"
**Solution**: App must start within 10 minutes
- Pre-download models
- Optimize imports
- Use lazy loading

### Issue: Large files rejected
**Solution**: Use Git LFS or external storage

## Alternative: Deploy Locally

If cloud deployment is challenging, deploy locally:

### Using ngrok (Public URL)
```bash
# Install ngrok from https://ngrok.com/
ngrok http 8501
```

### Using Docker
See `docker-deployment.md` for containerized deployment

## Files to Include in Repository

```
.
├── app.py
├── model_inference.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
├── xlstm_100hz_parallel_final.ckpt (via LFS or download)
└── normalization_params.npz
```

## Files to Exclude (.gitignore)

Create `.gitignore`:
```
__pycache__/
*.pyc
*.pyo
.venv/
.env
.streamlit/secrets.toml
*.log
.DS_Store
sample_ecg.npy
sample_ecg.csv
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Handle large model files (LFS or cloud storage)
3. ✅ Deploy to Streamlit Community Cloud
4. ✅ Test with sample data
5. ✅ Share your app URL!

## Support

- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/
- GitHub Issues: Create in your repo

---

**Your app will be available at:**
`https://YOUR_USERNAME-ecg-classifier-app-main-app-xyz123.streamlit.app`
