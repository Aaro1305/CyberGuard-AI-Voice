import os
import streamlit as st
import pandas as pd
from backend import analyze_audio_forensics
from database import init_db, save_scan, get_all_scans, delete_scan, clear_all_scans

# ---------------------------------------------------------
# 1. Page Configuration & Database Initialization
# ---------------------------------------------------------
st.set_page_config(
    page_title="CyberGuard | AI Voice Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# ---------------------------------------------------------
# 2. Premium Light Mode CSS Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Application Theme (Light Mode) */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header Banner Styling */
    .header-box {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
    }
    .header-title {
        color: #1e3a8a;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-subtitle {
        color: #475569;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 500;
    }
    .sih-badge {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }

    /* Metric Cards Styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 4px;
    }

    /* Forensic Verdict Cards */
    .report-card-fake {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.08);
    }
    .report-card-real {
        background: #ecfdf5;
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }

    /* Streamlit Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        color: #475569;
        font-weight: 600;
        padding: 0 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .stTabs [aria-selected="true"] {
        background: #eff6ff !important;
        border: 2px solid #2563eb !important;
        color: #1d4ed8 !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Top Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 class="header-title">🛡️ CyberGuard Intelligence</h1>
        <span class="sih-badge">SIH Forensic Prototype</span>
    </div>
    <p class="header-subtitle">AI-Powered Deepfake Voice Audio Detection & Scam Forensic Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Navigation Tabs
# ---------------------------------------------------------
tab_scan, tab_history = st.tabs(["🔍 Forensic Audio Scanner", "📜 Scan History & Analytics"])

# =========================================================
# TAB 1: FORENSIC SCANNER
# =========================================================
with tab_scan:
    sidebar_col, main_col = st.columns([1, 2.8])

    with sidebar_col:
        st.markdown("""
        <div class="metric-card" style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-weight: 700; color: #1e3a8a;">⚙️ System Status</span>
                <span style="background: #10b981; width: 10px; height: 10px; border-radius: 50%; display: inline-block;"></span>
            </div>
            <p style="color: #059669; font-weight: 700; margin: 8px 0 0 0;">ONLINE / ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎛️ Analysis Engines")
        st.checkbox("Spectral Flatness Analyzer", value=True, disabled=True)
        st.checkbox("Zero Crossing Artifact Detector", value=True, disabled=True)
        st.checkbox("MFCC Texture Classifier", value=True, disabled=True)
        
        st.markdown("---")
        st.markdown("**Team CyberGuard**")
        st.caption("Smart India Hackathon (SIH) Forensic Prototype")

    with main_col:
        st.subheader("🎙️ Forensic Audio Upload")
        st.write("Upload an intercepted call recording or voice sample (`.wav`, `.mp3`, `.flac`) for AI cloning analysis.")
        
        uploaded_file = st.file_uploader("Drag and drop audio file here", type=["wav", "mp3", "flac"])
        
        if uploaded_file is None:
            st.info("💡 **Instructions:** Select an audio file above and click **Run Deepfake Analysis** to initiate spectral checks.")
            st.button("🚀 Run Deepfake Analysis", disabled=True, width="stretch")
        else:
            st.success(f"✅ **File Loaded:** `{uploaded_file.name}` ({uploaded_file.size / 1024:.1f} KB)")
            
            # Audio Playback
            st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
            
            if st.button("🚀 Run Deepfake Analysis", width="stretch", type="primary"):
                with st.spinner("🔍 Extracting acoustic features, spectral flatness, and MFCCs..."):
                    # Save temporary file for Librosa processing
                    os.makedirs("uploads", exist_ok=True)
                    temp_file_path = os.path.join("uploads", uploaded_file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Call AI Forensic Engine in backend.py
                    results = analyze_audio_forensics(temp_file_path)
                    
                    st.markdown("---")
                    st.subheader("📊 Forensic Scan Report")
                    
                    if "error" in results:
                        st.error(f"❌ Audio Analysis Error: {results['error']}")
                        st.warning("Scan result was not saved because AI prediction failed.")
                    else:
                        conf_val = float(results["confidence"].replace("%", ""))
                        is_fake = results.get("is_fake", False)
                        
                        # Save complete scan to SQLite database
                        save_scan(
                            filename=uploaded_file.name,
                            verdict=results["verdict"],
                            confidence=conf_val,
                            risk_level=results["risk_level"],
                            file_path=temp_file_path,
                            spectral_flatness=results["spectral_flatness"],
                            zero_crossing_rate=results["zero_crossing_rate"],
                            mfcc_mean=results["mfcc_mean"]
                        )
                        
                        # Display Verdict Card
                        card_class = "report-card-fake" if is_fake else "report-card-real"
                        verdict_color = "#dc2626" if is_fake else "#059669"
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-size: 0.9rem; font-weight: 700; color: {verdict_color}; text-transform: uppercase;">Forensic Verdict</span>
                                    <h2 style="margin: 4px 0 0 0; color: #0f172a;">{results['verdict']}</h2>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 0.9rem; color: #64748b; font-weight: 600;">Cloning Confidence</span>
                                    <h2 style="margin: 4px 0 0 0; color: {verdict_color};">{results['confidence']}</h2>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Detailed Acoustic Feature Metrics
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Risk Level", results["risk_level"])
                        m2.metric("Spectral Flatness", results["spectral_flatness"])
                        m3.metric("Zero Crossing Rate", results["zero_crossing_rate"])
                        m4.metric("MFCC Texture Mean", results["mfcc_mean"])
                        
                        st.success("💾 Complete scan results automatically stored in local SQLite database!")

# =========================================================
# TAB 2: SCAN HISTORY & ANALYTICS
# =========================================================
with tab_history:
    st.subheader("📜 Forensic History & Database Logs")
    
    scans = get_all_scans()
    
    if not scans:
        st.info("No scan history records found in SQLite database yet. Perform a scan in the Scanner tab to populate history.")
    else:
        df = pd.DataFrame(scans)
        
        # Summary Analytics Cards
        total_scans = len(df)
        fake_count = len(df[df['verdict'].str.contains("DEEPFAKE", na=False)])
        real_count = total_scans - fake_count
        fake_percentage = (fake_count / total_scans * 100) if total_scans > 0 else 0
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Scans</div>
                <div class="metric-value" style="color: #2563eb;">{total_scans}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Deepfakes Flagged</div>
                <div class="metric-value" style="color: #dc2626;">{fake_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Authentic Human</div>
                <div class="metric-value" style="color: #059669;">{real_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">High Risk Rate</div>
                <div class="metric-value" style="color: #d97706;">{fake_percentage:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Actions: CSV Export and Clear All
        col_act1, col_act2 = st.columns([4, 1])
        with col_act1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export History to CSV",
                data=csv_data,
                file_name="cyberguard_scans_report.csv",
                mime="text/csv",
                type="secondary"
            )
        with col_act2:
            if st.button("🗑️ Clear All History", type="primary"):
                clear_all_scans()
                st.rerun()
                
        st.markdown("### 📋 Detailed Records Table")
        
        # Reorder and format display columns
        display_df = df[[
            "id", "filename", "verdict", "confidence", "risk_level", 
            "spectral_flatness", "zero_crossing_rate", "mfcc_mean", "scan_timestamp", "file_path"
        ]].rename(columns={
            "id": "ID",
            "filename": "Filename",
            "verdict": "Verdict",
            "confidence": "Confidence (%)",
            "risk_level": "Risk Level",
            "spectral_flatness": "Spectral Flatness",
            "zero_crossing_rate": "Zero Crossing Rate",
            "mfcc_mean": "MFCC Mean",
            "scan_timestamp": "Timestamp",
            "file_path": "File Path"
        })
        
        st.dataframe(
            display_df,
            width="stretch",
            column_config={
                "Confidence (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Timestamp": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss")
            }
        )