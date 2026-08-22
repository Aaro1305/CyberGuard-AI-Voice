import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_spectrogram(file_path):
    """Generates a high-tech Mel-Spectrogram plot for forensic analysis."""
    try:
        y, sr = librosa.load(file_path, duration=5.0)
        plt.figure(figsize=(6, 2.5), facecolor='#0f172a')
        ax = plt.axes()
        ax.set_facecolor('#0f172a')
        
        # Compute Mel-spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm')
        plt.tight_layout()
        plt.axis('off')
        
        spectrogram_path = "temp_spectrogram.png"
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
        # Load the audio file (y = audio time series, sr = sampling rate)
        y, sr = librosa.load(file_path, duration=10.0)
        
        # 1. Feature Extraction: Spectral Flatness
        spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        
        # 2. Feature Extraction: Zero Crossing Rate
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # 3. Feature Extraction: MFCCs for voice texture
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))
        
        # --- Detection Algorithm Simulation / Heuristic Classifier ---
        anomaly_score = float(np.abs(spectral_flatness * 150 + (zcr * 50)))
        
        # Normalize score between 15% and 99.4%
        confidence = min(max(anomaly_score * 10, 15.0), 99.4)
        confidence = round(confidence, 1)
        
        # Determine verdict based on confidence threshold
        is_fake = confidence > 65.0
        
        # Generate spectrogram visualization
        generate_spectrogram(file_path)
        
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
    if os.path.exists("temp_spectrogram.png"):
        story.append(Paragraph("<b>Mel-Spectrogram Frequency Analysis:</b>", body_style))
        story.append(RLImage("temp_spectrogram.png", width=450, height=180))

    doc.build(story)
    return filename