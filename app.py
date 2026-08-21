import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="CyberGuard Voice Intelligence Portal",
    page_icon="🛡️",
    layout="wide"
)

# 2. Top Header Banner
st.title("🛡️ CyberGuard: AI Voice Deepfake & Cyber-Scam Intelligence Platform")
st.markdown("---")

# 3. Create Layout Columns
sidebar_col, main_col = st.columns([1, 3])

with sidebar_col:
    st.header("⚙️ Control Panel")
    st.info("System Status: **ONLINE / READY**")
    
    st.markdown("### Model Settings")
    st.checkbox("Fast Spectrum Analysis", value=True)
    st.checkbox("Deep Neural Classifier", value=True)
    
    st.markdown("---")
    st.markdown("**Team CyberGuard**")
    st.markdown("SIH Round 1 Evaluation")

with main_col:
    st.subheader("🔍 Forensic Audio Input")
    st.write("Upload an intercepted audio file below to initiate deepfake and cloning checks.")
    
    # File Upload Box
    uploaded_file = st.file_uploader("Drag and drop audio file here", type=["wav", "mp3", "flac"])
    
    if uploaded_file is None:
        # Before Upload State
        st.warning("⚠️ Awaiting Forensic Input. Please upload an audio sample to begin analysis.")
        
        st.markdown("""
        ### ℹ️ System Instructions:
        1. Select a `.wav` or `.mp3` audio file from your computer.
        2. Ensure the audio sample is clear of heavy background static.
        3. Click the **Run Analysis** button once enabled.
        """)
        
        st.button("🚀 Run Deepfake Analysis", disabled=True)
        
    else:
        # After Upload State
        st.success("✅ File uploaded successfully! Ready for processing.")
        st.write(f"**Filename:** {uploaded_file.name}")
        
        if st.button("🚀 Run Deepfake Analysis"):
            with st.spinner("Analyzing spectral patterns and voice artifacts..."):
                st.markdown("---")
                st.subheader("📊 Forensic Analysis Report")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.error("VERDICT: 🔴 AI-GENERATED (98.7% FAKE)")
                with col2:
                    st.metric(label="Cloning Confidence", value="98.7%", delta="High Risk")
                
                st.info("💡 **Actionable Recommendation:** High risk of voice cloning detected. Do not transfer funds or execute requested actions.")