import os
import subprocess
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def ensure_wav_format(file_path):
    """
    Checks if the audio file format is readable by librosa.
    If it is WebM/OGG/MP3/M4A from browser recording or non-standard format,
    converts it to a clean WAV audio file using imageio_ffmpeg.
    """
    try:
        import soundfile as sf
        info = sf.info(file_path)
        if info.format == 'WAV' and info.frames > 0:
            return file_path
    except Exception:
        pass

    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        converted_path = os.path.splitext(file_path)[0] + "_converted.wav"
        
        cmd = [
            ffmpeg_exe, "-y",
            "-i", file_path,
            "-ar", "22050",
            "-ac", "1",
            converted_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(converted_path) and os.path.getsize(converted_path) > 0:
            return converted_path
    except Exception as e:
        print(f"Format conversion warning: {e}")

    return file_path

def generate_spectrogram(file_path):
    """Generates a high-tech Mel-Spectrogram plot for forensic analysis."""
    try:
        valid_path = ensure_wav_format(file_path)
        y, sr = librosa.load(valid_path, duration=5.0)
        plt.figure(figsize=(6, 2.5), facecolor='#0f172a')
        ax = plt.axes()
        ax.set_facecolor('#0f172a')
        
        # Compute Mel-spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm')
        plt.tight_layout()
        plt.axis('off')
        
        os.makedirs("uploads", exist_ok=True)
        spectrogram_path = os.path.join("uploads", "temp_spectrogram.png")
        plt.savefig(spectrogram_path, bbox_inches='tight', pad_inches=0, facecolor='#0f172a')
        plt.close()
        return spectrogram_path
    except Exception:
        return None

def analyze_audio_forensics(file_path):
    """
    Analyzes an audio file using Librosa to detect deepfake characteristics,
    such as spectral flatness and unnatural frequency anomalies.
    """
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return {"error": "The recorded or uploaded audio file is empty. Please record/upload again."}

        # Convert webm/ogg or non-standard browser recording bytes to WAV
        valid_audio_path = ensure_wav_format(file_path)

        # Load the audio file (y = audio time series, sr = sampling rate)
        y, sr = librosa.load(valid_audio_path, duration=10.0)
        
        if len(y) == 0:
            return {"error": "Audio stream contains no sound samples. Please try recording again."}
        
        # Trim leading/trailing silence for precise feature analysis
        y_trimmed, _ = librosa.effects.trim(y, top_db=25)
        if len(y_trimmed) < sr * 0.5:
            y_trimmed = y
            
        dur = float(librosa.get_duration(y=y_trimmed, sr=sr))

        # 1. Feature Extraction: Spectral Flatness (measures noise vs tonal content)
        flatness_arr = librosa.feature.spectral_flatness(y=y_trimmed)
        spectral_flatness = float(np.mean(flatness_arr))
        
        # 2. Feature Extraction: Zero Crossing Rate
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y_trimmed)))
        
        # 3. Feature Extraction: MFCC Texture & Standard Deviation
        mfccs_arr = librosa.feature.mfcc(y=y_trimmed, sr=sr, n_mfcc=13)
        mfccs = float(np.mean(mfccs_arr))
        mfcc_std = float(np.std(mfccs_arr))

        # 4. Feature Extraction: Harmonic Energy Ratio
        y_harmonic, y_percussive = librosa.effects.hpss(y_trimmed)
        harmonic_energy = np.sum(y_harmonic ** 2)
        total_energy = np.sum(y_trimmed ** 2) + 1e-8
        harmonic_ratio = float(harmonic_energy / total_energy)

        # 5. Feature Extraction: Pitch Modulation (F0 dynamics)
        pitches, magnitudes = librosa.piptrack(y=y_trimmed, sr=sr)
        voiced_pitches = pitches[pitches > 50]
        pitch_std = float(np.std(voiced_pitches)) if len(voiced_pitches) > 10 else 0.0

        # --- Calibrated Multi-Feature Evidence Scorer ---
        anomaly_points = 0.0
        
        # Feature 1: Spectral Flatness Anomaly (Vocoder noise artifacts)
        if spectral_flatness > 0.05:
            anomaly_points += 3.5
        elif spectral_flatness > 0.02:
            anomaly_points += 1.5
            
        # Feature 2: MFCC Variance Anomaly (Flat/Robotic vs natural dynamic speech)
        if mfcc_std < 50.0:
            anomaly_points += 2.5
        elif mfcc_std < 80.0:
            anomaly_points += 1.0
            
        # Feature 3: Monotone Pitch / Lack of Natural Prosody
        if dur > 1.5 and pitch_std < 10.0:
            anomaly_points += 2.5
            
        # Feature 4: Unnatural Harmonic Energy Ratio
        if harmonic_ratio < 0.15:
            anomaly_points += 2.0

        is_fake = anomaly_points >= 3.5
        
        if is_fake:
            confidence = min(65.0 + (anomaly_points - 3.5) * 8.0, 98.5)
            verdict_str = "AI-GENERATED (DEEPFAKE DETECTED)"
            risk_str = "High Risk"
        else:
            confidence = min(65.0 + (3.5 - anomaly_points) * 9.5, 98.5)
            verdict_str = "AUTHENTIC HUMAN VOICE"
            risk_str = "Low Risk"

        confidence = round(confidence, 1)

        # Generate spectrogram visualization
        generate_spectrogram(file_path)
        
        analysis_results = {
            "verdict": verdict_str,
            "confidence": f"{confidence}%",
            "risk_level": risk_str,
            "spectral_flatness": f"{spectral_flatness:.5f}",
            "zero_crossing_rate": f"{zcr:.5f}",
            "mfcc_mean": f"{mfccs:.2f}",
            "is_fake": is_fake
        }
        
        return analysis_results

    except Exception as e:
        return {"error": str(e)}

def generate_pdf_report(results, filename="CyberGuard_Forensic_Report.pdf"):
    """Generates a professional forensic PDF report including the spectrogram image."""
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    story.append(Paragraph("CyberGuard AI | Forensic Audio Intelligence Report", title_style))
    story.append(Paragraph("<b>Confidential Forensic Evaluation</b>", body_style))
    story.append(Spacer(1, 10))

    # Results Breakdown
    story.append(Paragraph(f"<b>Verdict:</b> {results.get('verdict')}", body_style))
    story.append(Paragraph(f"<b>Cloning Confidence:</b> {results.get('confidence')}", body_style))
    story.append(Paragraph(f"<b>Risk Level:</b> {results.get('risk_level')}", body_style))
    story.append(Paragraph(f"<b>Spectral Flatness:</b> {results.get('spectral_flatness')}", body_style))
    story.append(Paragraph(f"<b>Zero Crossing Rate:</b> {results.get('zero_crossing_rate')}", body_style))
    story.append(Spacer(1, 15))

    # Embed Spectrogram Image if it exists
    spec_img_path = os.path.join("uploads", "temp_spectrogram.png")
    if os.path.exists(spec_img_path):
        story.append(Paragraph("<b>Mel-Spectrogram Frequency Analysis:</b>", body_style))
        story.append(RLImage(spec_img_path, width=450, height=180))

    doc.build(story)
    return filename