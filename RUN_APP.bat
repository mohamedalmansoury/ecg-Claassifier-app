@echo off
echo ========================================
echo   ECG CLASSIFIER - RUN LOCALLY
echo ========================================
echo.

set KMP_DUPLICATE_LIB_OK=TRUE

python -c "import streamlit" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Streamlit...
    pip install streamlit
)

echo Starting ECG Classifier App...
echo.
echo The app will open in your browser at:
echo   http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo ========================================
echo.

streamlit run app.py

pause
