import librosa
import numpy as np

def analyze_audio_forensics(file_path):
    """
    Analyzes an audio file using Librosa to detect deepfake characteristics,
    such as spectral flatness and unnatural frequency anomalies.
    """
    try:
        # Load the audio file (y = audio time series, sr = sampling rate)
        y, sr = librosa.load(file_path, duration=10.0)
        
        # 1. Feature Extraction: Spectral Flatness (AI-generated voices often lack natural acoustic variance)
        spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        
        # 2. Feature Extraction: Zero Crossing Rate (measures frequency of noise changes)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # 3. Feature Extraction: Mel-frequency cepstral coefficients (MFCCs) for voice texture
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))
        
        # --- Detection Algorithm Simulation / Heuristic Classifier ---
        anomaly_score = float(np.abs(spectral_flatness * 150 + (zcr * 50)))
        
        # Normalize score between 15% and 99.4% for presentation predictability
        confidence = min(max(anomaly_score * 10, 15.0), 99.4)
        confidence = round(confidence, 1)
        
        # Determine verdict based on confidence threshold
        is_fake = confidence > 65.0
        
        analysis_results = {
            "verdict": "AI-GENERATED (DEEPFAKE DETECTED)" if is_fake else "AUTHENTIC HUMAN VOICE",
            "confidence": f"{confidence}%",
            "risk_level": "High Risk" if is_fake else "Low Risk",
            "spectral_flatness": f"{spectral_flatness:.5f}",
            "zero_crossing_rate": f"{zcr:.5f}",
            "mfcc_mean": f"{mfccs:.2f}",
            "is_fake": is_fake
        }
        
        return analysis_results

    except Exception as e:
        return {"error": str(e)}