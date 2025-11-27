@echo off
echo ================================================
echo Git Repository Setup for Streamlit Deployment
echo ================================================
echo.

where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please download and install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed. Proceeding with setup...
echo.

echo [1/6] Initializing Git repository...
git init

echo [2/6] Adding files to Git...
git add .

echo [3/6] Creating initial commit...
git commit -m "Initial commit: ECG classifier deployment"

echo.
echo [4/6] Using your GitHub repository:
echo    https://github.com/mohamedalmansoury/New_ecg_classiification.git
echo.

echo [5/6] Adding remote and pushing to GitHub...
git remote add origin https://github.com/mohamedalmansoury/New_ecg_classiification.git
git branch -M main

echo.
echo Pushing to GitHub (you may need to authenticate)...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo SUCCESS! Repository pushed to GitHub
    echo ================================================
    echo.
    echo Next steps:
    echo 1. Go to https://share.streamlit.io/
    echo 2. Sign in with GitHub
    echo 3. Click "New app"
    echo 4. Select: mohamedalmansoury/New_ecg_classiification
    echo 5. Main file: app.py
    echo 6. Click "Deploy"
    echo.
    echo Your app will be at:
    echo https://mohamedalmansoury-new-ecg-classiification-app-xyz.streamlit.app
    echo.
) else (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo Possible issues:
    echo - Repository not created yet
    echo - Authentication failed
    echo - Model files too large (need Git LFS)
    echo.
    echo For large files, see DEPLOYMENT_GUIDE.md
)

pause
