# 🚀 QUICK START - ECG Classifier Deployment

## 📁 This Folder Contains Everything You Need!

### ✅ Essential Files (All Ready!)
1. `app.py` - Main Streamlit application
2. `model_inference.py` - Model loading code
3. `utils.py` - Data preprocessing
4. `requirements.txt` - Python packages needed
5. `xlstm_100hz_parallel_final.ckpt` - Trained model
6. `normalization_params.npz` - Normalization parameters
7. `.gitignore` - Files to exclude from Git

---

## 🎯 DEPLOYMENT IN 3 STEPS

### Step 1: Test Locally (2 minutes)
```bash
# Open PowerShell in this folder and run:
streamlit run app.py
```
Opens at: http://localhost:8501

### Step 2: Push to GitHub (5 minutes)
```bash
# Run the automated script:
.\setup_github.bat

# It will ask for your GitHub username
# Then automatically push everything to GitHub
```

### Step 3: Deploy to Streamlit Cloud (3 minutes)
1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub repository
4. Select: `app.py` as main file
5. Click "Deploy"
6. Done! ✨

---

## 📋 What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | The web interface (Streamlit UI) |
| `model_inference.py` | Loads the AI model & makes predictions |
| `utils.py` | Cleans & prepares ECG signals |
| `requirements.txt` | Lists all Python packages needed |
| `.gitignore` | Tells Git what NOT to upload |
| `xlstm_100hz_parallel_final.ckpt` | The trained AI model (170MB) |
| `normalization_params.npz` | Signal normalization values |
| `setup_github.bat` | Automated Git setup script |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment instructions |
| `README.md` | Project documentation |

---

## 🎮 How to Use the App

1. **Upload ECG file** (.npy or .csv format)
2. **Enter patient info** (age, sex)
3. **Get predictions** for 5 heart conditions:
   - NORM - Normal ECG
   - MI - Myocardial Infarction (Heart Attack)
   - STTC - ST/T Change
   - CD - Conduction Disturbance
   - HYP - Hypertrophy

---

## ⚠️ Large File Warning

The model file (`xlstm_100hz_parallel_final.ckpt`) is ~170MB.

**GitHub limits files to 100MB**, so you need **Git LFS**:

```bash
# Install Git LFS (one-time setup)
git lfs install

# Track large files
git lfs track "*.ckpt"

# Commit and push
git add .gitattributes
git commit -m "Add LFS"
git push
```

---

## 🆘 Quick Troubleshooting

### Problem: "streamlit: command not found"
**Fix:** Install Streamlit
```bash
pip install streamlit
```

### Problem: "Git not found"
**Fix:** Install Git from https://git-scm.com/

### Problem: "Model file too large"
**Fix:** Use Git LFS (see above) OR host model elsewhere

### Problem: "DLL load failed"
**Fix:** This is already fixed in the code! Just run the app.

---

## 📞 Need More Help?

- **Detailed Guide**: Open `DEPLOYMENT_GUIDE.md`
- **Streamlit Docs**: https://docs.streamlit.io/
- **Git LFS Info**: https://git-lfs.github.com/

---

## ✨ You're All Set!

Everything is ready in this folder. Just run:
```bash
.\setup_github.bat
```

Then deploy to Streamlit Cloud!

🎉 **Good luck with your deployment!**
