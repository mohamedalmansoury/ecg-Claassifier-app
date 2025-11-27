# ECG Classification with Parallel xLSTM

Deep learning application for classifying cardiac conditions from ECG signals using Parallel xLSTM architecture.

##  Quick Start

### Run Locally
```bash
streamlit run app.py
```

### Deploy to Cloud
See `START_HERE.md` for step-by-step guide

## 📊 Features

- 🫀 Classifies 5 cardiac conditions
- 📁 Supports .npy, .csv, and WFDB formats
- 🎨 Interactive web interface
- 📈 Real-time probability visualization

## 🏥 Classifications

1. **NORM** - Normal ECG
2. **MI** - Myocardial Infarction
3. **STTC** - ST/T Change
4. **CD** - Conduction Disturbance
5. **HYP** - Hypertrophy

## 🔧 Technical Stack

- **Framework**: PyTorch, Streamlit
- **Model**: Parallel xLSTM (sLSTM + mLSTM)
- **Dataset**: PTB-XL (22k+ ECG recordings)
- **Input**: 1000 timesteps × 12 leads @ 100Hz

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🎮 Usage

1. Upload ECG signal file
2. Enter patient metadata (age, sex {0: Male, 1: Female}) 
3. View predictions and probabilities

## 📁 Project Structure

```
.
├── app.py                 # Main Streamlit app
├── model_inference.py     # Model loading & inference
├── utils.py               # Preprocessing utilities
├── requirements.txt       # Dependencies
├── xlstm_100hz_parallel_final.ckpt  # Model weights
└── normalization_params.npz         # Normalization params
```

## 👤 Author

Mohamed Ahmed AL Mansoury - 2025

## 🙏 Acknowledgments

- PTB-XL dataset creators
- xlstm library developers
- Streamlit team
