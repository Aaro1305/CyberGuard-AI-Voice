import streamlit as st
import os
import pandas as pd
from backend import analyze_audio_forensics, generate_pdf_report
from database import init_db, save_scan, get_all_scans, clear_all_scans
from streamlit_mic_recorder import mic_recorder

# Page Configuration
st.set_page_config(
    page_title="Vocalis AI | Voice Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
init_db()

# Custom CSS to transform Streamlit's file uploader box and polish the results dashboard
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 4px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    /* Hide default label */
    .stFileUploader label {
        display: none;
    }
    /* Style the main file uploader container box */
    [data-testid="stFileUploader"] {
        background-color: #0f172a;
        padding: 30px;
        border-radius: 12px;
        border: 2px dashed #334155;
        text-align: center;
    }
    /* Style the inner upload drop section container */
    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
        border: none !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    /* Style the upload button inside the box */
    [data-testid="stFileUploader"] button {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 500;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #334155 !important;
        border-color: #64748b !important;
    }
    /* Style instructional text inside uploader */
    [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] span {
        color: #94a3b8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar UI
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    st.success("ONLINE / ACTIVE")
    
    st.markdown("---")
    st.markdown("### 🔍 Analysis Engines")
    st.markdown("""
    - Spectral Flatness Analyzer  
    - Zero Crossing Artifact Detector  
    - MFCC Texture Classifier  
    """)
    
    st.markdown("---")
    st.markdown("### 🛡️ Team Vocalis AI")

# Main Navigation Tabs (Home & Overview is FIRST so it opens by default)
tab_home, tab_scanner, tab_history = st.tabs([
    "🏠 Home & Overview", 
    "🎙️ Forensic Audio Scanner", 
    "📊 Scan History"
])

# ==================== TAB 1: HOME & OVERVIEW ====================
with tab_home:
    st.markdown("""
        <div style="padding: 30px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border-radius: 8px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <h1 style="color: white; margin-bottom: 15px; font-size: 32px; font-weight: 800; letter-spacing: 0.5px;">
                🛡️ Vocalis AI | Voice Intelligence Platform
            </h1>
            <p style="font-size: 16px; line-height: 1.6; color: #e2e8f0; margin-bottom: 20px;">
                <b>Our Aim:</b> To engineer a robust, accessible, and high-precision acoustic defense platform that exposes synthetic voice cloning and prevents audio deepfake fraud. We aim to empower everyday citizens, organizations, and authorities to instantly verify intercepted calls and neutralize AI-driven social engineering attacks.
            </p>
            <div style="display: flex; gap: 20px; font-size: 14px;">
                <span style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 4px;">🔍 Multi-Engine Forensic Analysis</span>
                <span style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 4px;">📊 Mel-Spectrogram Visualization</span>
                <span style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 4px;">📑 Official PDF Reporting</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛡️ How to Stay Safe from AI Voice Fraud & Vishing Calls")
    st.caption("Practical defense strategies to protect yourself, your family, and your organization against synthetic voice impersonation.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; height: 180px;">
            <h4>🔒 Set a Family Safe Word</h4>
            <p style="font-size: 12px; color: #666;">Establish a secret verbal passcode known only to trusted family members to verify sudden emergency or ransom calls.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; height: 180px;">
            <h4>📞 Verify via Callback</h4>
            <p style="font-size: 12px; color: #666;">If someone claiming to be a relative or official asks for urgent money, hang up and call them back on their known number.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; height: 180px;">
            <h4>🎙️ Limit Voice Exposure</h4>
            <p style="font-size: 12px; color: #666;">Be cautious of posting high-definition audio clips or public voice samples on social media that cloners can exploit.</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0; height: 180px;">
            <h4>⚠️ Question Urgency</h4>
            <p style="font-size: 12px; color: #666;">Scammers rely on panic. Always stay calm and independently verify unexpected financial requests or threats.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("👉 Ready to test a file? Switch to the **'Forensic Audio Scanner'** tab above to upload and verify any suspicious recording.")

# ==================== TAB 2: FORENSIC AUDIO SCANNER ====================
with tab_scanner:
    st.markdown("""
        <div style="margin-bottom: 15px;">
            <h3 style="color: #1e3c72; margin-bottom: 5px;">🎙️ Forensic Audio Scanner Workspace</h3>
            <p style="color: #64748b; font-size: 14px;">Select an input method below to run multi-engine forensic cloning checks on audio files or live voice recordings.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input selection: File Upload vs Microphone Recording
    input_method = st.radio(
        "Choose Input Method:",
        ["📁 Upload Audio File", "🎙️ Record from Microphone"],
        horizontal=True
    )
    
    file_path = None
    target_filename = None
    should_run_analysis = False

    if input_method == "📁 Upload Audio File":
        uploaded_file = st.file_uploader("", type=["wav", "mp3", "flac", "m4a", "mp4"])

        if uploaded_file is not None:
            os.makedirs("uploads", exist_ok=True)
            target_filename = uploaded_file.name
            file_path = os.path.join("uploads", target_filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File Loaded Successfully: {target_filename}")
            st.audio(file_path)

            if st.button("🚀 Run Deepfake Analysis", type="primary"):
                should_run_analysis = True

    else:
        st.markdown("""
            <div style="background: #0f172a; padding: 24px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; color: white;">
                <h4 style="margin-top: 0; color: #f8fafc; font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    🎙️ Live Microphone Recorder
                </h4>
                <p style="color: #94a3b8; font-size: 13px; margin-bottom: 15px;">
                    Click <b>Start Recording</b> to capture your voice. Click <b>Stop Recording</b> when complete.
                </p>
            </div>
        """, unsafe_allow_html=True)

        audio_recorded = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹ Stop Recording",
            key="mic_recorder",
            just_once=False,
            use_container_width=True
        )

        if audio_recorded is not None and "bytes" in audio_recorded and len(audio_recorded["bytes"]) > 0:
            os.makedirs("uploads", exist_ok=True)
            target_filename = "microphone_recording.wav"
            file_path = os.path.join("uploads", target_filename)
            with open(file_path, "wb") as f:
                f.write(audio_recorded["bytes"])
            st.session_state["active_mic_file"] = file_path

        if "active_mic_file" in st.session_state and st.session_state["active_mic_file"] and os.path.exists(st.session_state["active_mic_file"]):
            file_path = st.session_state["active_mic_file"]
            target_filename = os.path.basename(file_path)

            st.markdown("""
                <div style="background: #1e293b; padding: 16px 20px; border-radius: 8px; border: 1px solid #10b981; color: #34d399; font-weight: 600; font-size: 14px; margin-top: 15px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between;">
                    <span>✅ Recording Complete! Play back audio below or click "Analyze Recording".</span>
                    <span style="background: #065f46; color: #a7f3d0; padding: 4px 10px; border-radius: 20px; font-size: 11px; text-transform: uppercase;">READY FOR ANALYSIS</span>
                </div>
            """, unsafe_allow_html=True)

            st.audio(file_path)

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔄 Record Again", use_container_width=True):
                    st.session_state["active_mic_file"] = None
                    if "mic_recorder" in st.session_state:
                        del st.session_state["mic_recorder"]
                    st.rerun()

            with col_btn2:
                if st.button("🔍 Analyze Recording", type="primary", use_container_width=True):
                    should_run_analysis = True

    if should_run_analysis and file_path is not None and os.path.exists(file_path):
        with st.spinner("Executing forensic acoustic analysis... Please wait."):
            results = analyze_audio_forensics(file_path)
            
            if "error" in results:
                st.error(f"Analysis Error: {results['error']}")
            else:
                conf_val = float(results['confidence'].replace('%', ''))

                scan_id = save_scan(
                    filename=target_filename,
                    verdict=results['verdict'],
                    confidence=conf_val,
                    risk_level=results['risk_level'],
                    file_path=file_path,
                    spectral_flatness=results['spectral_flatness'],
                    zero_crossing_rate=results['zero_crossing_rate'],
                    mfcc_mean=results['mfcc_mean']
                )

                st.markdown("---")
                
                # Professional Forensic Dashboard Results Header
                st.markdown("""
                    <div style="background: #1e293b; padding: 15px 20px; border-radius: 8px; color: white; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                        <h3 style="margin: 0; color: #f8fafc; font-size: 20px;">📋 Forensic Intelligence Report</h3>
                        <span style="background: #3b82f6; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600;">VERIFIED SCAN</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metric Cards with proper spacing and styling
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <p style="color: #64748b; font-size: 13px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Verdict</p>
                            <h3 style="color: #0f172a; font-size: 20px; font-weight: 700; margin: 0;">{results['verdict']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <p style="color: #64748b; font-size: 13px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Confidence Score</p>
                            <h3 style="color: #0f172a; font-size: 20px; font-weight: 700; margin: 0;">{results['confidence']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_c:
                    risk_color = "#10b981" if "Low" in results['risk_level'] else "#ef4444"
                    st.markdown(f"""
                        <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <p style="color: #64748b; font-size: 13px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Risk Level</p>
                            <h3 style="color: {risk_color}; font-size: 20px; font-weight: 700; margin: 0;">{results['risk_level']}</h3>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Acoustic Metric Breakdown Box
                st.markdown("### 📊 Acoustic Metric Breakdown")
                st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 25px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                            <div>
                                <span style="color: #64748b; font-size: 12px; font-weight: 600;">Spectral Flatness</span>
                                <p style="font-family: monospace; font-size: 16px; color: #0f172a; font-weight: 600; margin: 5px 0 0 0;">{results['spectral_flatness']}</p>
                            </div>
                            <div>
                                <span style="color: #64748b; font-size: 12px; font-weight: 600;">Zero Crossing Rate</span>
                                <p style="font-family: monospace; font-size: 16px; color: #0f172a; font-weight: 600; margin: 5px 0 0 0;">{results['zero_crossing_rate']}</p>
                            </div>
                            <div>
                                <span style="color: #64748b; font-size: 12px; font-weight: 600;">MFCC Texture Mean</span>
                                <p style="font-family: monospace; font-size: 16px; color: #0f172a; font-weight: 600; margin: 5px 0 0 0;">{results['mfcc_mean']}</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Display generated Mel-Spectrogram image if available
                spec_img_path = os.path.join("uploads", "temp_spectrogram.png")
                if os.path.exists(spec_img_path):
                    st.markdown("### 📈 Mel-Spectrogram Frequency Analysis")
                    st.image(spec_img_path, caption="Generated Frequency Spectrogram", use_container_width=True)

                # PDF Report generation & Download button
                os.makedirs("uploads", exist_ok=True)
                pdf_filename = f"VocalisAI_Report_{scan_id}.pdf"
                pdf_filepath = os.path.join("uploads", pdf_filename)
                generate_pdf_report(results, pdf_filepath)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if os.path.exists(pdf_filepath):
                    with open(pdf_filepath, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Official Forensic Report (PDF)",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )

# ==================== TAB 3: SCAN HISTORY ====================
with tab_history:
    st.subheader("📊 Scan History Archive")
    st.caption("Review previous forensic logs saved in the local SQLite database.")
    
    scans = get_all_scans()

    if not scans:
        st.info("No scan history available yet. Run a scan in the **'Forensic Audio Scanner'** tab to populate records.")
    else:
        df = pd.DataFrame(scans)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Clear History Archive"):
            clear_all_scans()
            st.rerun()