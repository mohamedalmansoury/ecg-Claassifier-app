import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['CUDA_HOME'] = ''
os.environ['CUDA_LIB'] = ''

import streamlit as st
import torch
import numpy as np
import tempfile
import wfdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from model_inference import load_model_from_checkpoint
from utils import preprocess_input, load_normalization_params

CONFIG = {
    'input_shape': (1000, 12),
    'num_classes': 5,
    'metadata_dim': 2,
    'embedding_dim': 128,
    'slstm_hidden_size': 256,
    'mlstm_hidden_size': 256,
    'num_heads': 4,
    'dropout': 0.3,
    'batch_size': 32,
    'epochs': 14,
    'learning_rate': 0.001,
    'patience': 3,
}

CLASS_NAMES = ['NORM', 'MI', 'STTC', 'CD', 'HYP']

@st.cache_resource
def load_model(checkpoint_path, config):
    if not os.path.exists(checkpoint_path):
        st.error(f"Model checkpoint not found at {checkpoint_path}")
        return None
    
    try:
        model = load_model_from_checkpoint(checkpoint_path, config)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None

@st.cache_resource
def load_norm_params(params_path):
    if not os.path.exists(params_path):
        st.warning(f"Normalization params not found at {params_path}. Using raw signal.")
        return None, None
    try:
        return load_normalization_params(params_path)
    except Exception as e:
        st.warning(f"Error loading normalization params: {e}. Using raw signal.")
        return None, None

def main():
    st.title("ECG Classification with Parallel xLSTM")
    st.write("Upload an ECG data file to classify.")

    # Sidebar for Metadata
    st.sidebar.header("Patient Metadata")
    age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=60)
    sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
    sex_val = 1 if sex == "Male" else 0

    uploaded_files = st.file_uploader("Choose file(s)", type=['dat', 'hea', 'npy', 'csv'], accept_multiple_files=True)
    
    if not uploaded_files:
        uploaded_files = []
    elif not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]
    
    if len(uploaded_files) > 0:
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            signal = None
            
            try:
                file_names = [f.name for f in uploaded_files]
                
                if any(f.endswith('.npy') for f in file_names):
                    npy_file = [f for f in file_names if f.endswith('.npy')][0]
                    signal = np.load(os.path.join(temp_dir, npy_file))
                    
                elif any(f.endswith('.csv') for f in file_names):
                    csv_file = [f for f in file_names if f.endswith('.csv')][0]
                    signal = np.loadtxt(os.path.join(temp_dir, csv_file), delimiter=',')
                    
                elif any(f.endswith('.dat') for f in file_names):
                    dat_files = [f for f in file_names if f.endswith('.dat')]
                    hea_files = [f for f in file_names if f.endswith('.hea')]
                    
                    if not hea_files:
                        st.error("For WFDB format, please upload both .dat and .hea files together.")
                        return
                    
                    dat_file = dat_files[0]
                    record_name = dat_file.replace('.dat', '')
                    record_path = os.path.join(temp_dir, record_name)
                    
                    # Read using WFDB
                    signal, _ = wfdb.rdsamp(record_path)
                    st.success(f"Successfully loaded WFDB record: {record_name}")
                
                if signal is not None:
                    st.success(f"✓ File loaded successfully!")
                    st.write(f"Signal shape: {signal.shape}")
                    
                    if not isinstance(signal, np.ndarray):
                        signal = np.array(signal, dtype=np.float32)
                    
                    if len(signal.shape) != 2:
                        st.error(f"Expected 2D array, got shape {signal.shape}")
                        return
                        
                    if signal.shape[1] != 12 and signal.shape[0] != 12:
                        st.error(f"Expected 12 leads, got shape {signal.shape}")
                        return
                        
                    if signal.shape[1] != 12:
                        st.warning(f"Transposing signal from {signal.shape} to match expected format...")
                        signal = signal.T
                        
                    if signal.shape[0] != 1000:
                        st.warning(f"Adjusting timesteps from {signal.shape[0]} to 1000...")
                        if signal.shape[0] > 1000:
                            signal = signal[:1000, :]
                        else:
                            pad = np.zeros((1000 - signal.shape[0], 12), dtype=np.float32)
                            signal = np.vstack([signal, pad])
                    
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    parent_dir = os.path.dirname(script_dir)
                    
                    model_filename = "xlstm_100hz_parallel_final.ckpt"
                    model_path = None
                    for search_dir in [script_dir, parent_dir, os.getcwd()]:
                        test_path = os.path.join(search_dir, model_filename)
                        if os.path.exists(test_path):
                            model_path = test_path
                            break
                    
                    norm_filename = "normalization_params.npz"
                    norm_path = None
                    for search_dir in [script_dir, parent_dir, os.getcwd()]:
                        for name in [norm_filename, "normalization_params (1).npz"]:
                            test_path = os.path.join(search_dir, name)
                            if os.path.exists(test_path):
                                norm_path = test_path
                                break
                        if norm_path:
                            break
                    
                    if not model_path:
                        st.error(f"Model checkpoint '{model_filename}' not found. Please place it in the deployment folder.")
                        return
                    
                    if not norm_path:
                        st.warning("Normalization params not found. Using raw signal (may affect accuracy).")

                    model = load_model(model_path, CONFIG)
                    global_mean, global_std = load_norm_params(norm_path)
                    
                    if model:
                        metadata = [age, sex_val]
                        X, M = preprocess_input(signal, metadata, global_mean, global_std)
                        
                        X = torch.tensor(X, dtype=torch.float32).unsqueeze(0)
                        M = torch.tensor(M, dtype=torch.float32).unsqueeze(0)
                        
                        with torch.no_grad():
                            output = model(X, M)
                            probs = output.cpu().numpy()[0]
                        
                        st.markdown("---")
                        st.markdown("## 🎯 Prediction Results")
                        
                        max_idx = np.argmax(probs)
                        max_prob = probs[max_idx]
                        predicted_class = CLASS_NAMES[max_idx]
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.markdown(f"""
                            <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;'>
                                <h2 style='color: white; margin: 0; font-size: 2.5em;'>{predicted_class}</h2>
                                <p style='color: #f0f0f0; margin: 10px 0 0 0; font-size: 1.3em;'>Confidence: {max_prob*100:.1f}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("### 📊 All Class Probabilities")
                        
                        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
                        for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, probs)):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown(f"**{class_name}**")
                            with col2:
                                st.progress(float(prob))
                                st.caption(f"{prob*100:.2f}%")
                        
            except Exception as e:
                st.error(f"Error processing file: {e}")
                import traceback
                with st.expander("Show detailed error"):
                    st.code(traceback.format_exc())
                
                st.info("💡 Tip: If you're getting DLL errors, try saving your data as .npy format:\n```python\nimport numpy as np\nnp.save('ecg_signal.npy', your_signal_array)\n```")

if __name__ == "__main__":
    main()
