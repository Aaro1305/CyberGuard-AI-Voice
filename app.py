import streamlit as st
from audio_upload_security import validate_audio_upload  # 🔒 Sakshi's security module
from backend import analyze_audio_forensics  # AI teammate's detection function

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
   

with main_col:
    st.subheader("🔍 Forensic Audio Input")
    st.write("Upload an intercepted audio file below to initiate deepfake and cloning checks.")
    
    # File Upload Box
    uploaded_file = st.file_uploader("Drag and drop audio file here", type=["wav", "mp3", "flac", "mpeg"])
    
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
        # 🔒 SECURITY CHECK — runs the moment a file is uploaded, before anything else touches it
        is_valid, message, safe_path = validate_audio_upload(uploaded_file)

        if not is_valid:
            # Bad file: stop here. Never reaches the AI model. App doesn't crash.
            st.error(f"❌ Upload rejected: {message}")
            st.button("🚀 Run Deepfake Analysis", disabled=True)

        else:
            # After Upload State — file passed all security checks
            st.success("✅ File uploaded successfully and passed security checks!")
            st.write(f"**Filename:** {uploaded_file.name}")

            if st.button("🚀 Run Deepfake Analysis"):
                with st.spinner("Analyzing spectral patterns and voice artifacts..."):
                    # Hand the SAFE file path to the AI teammate's real function
                    results = analyze_audio_forensics(safe_path)

                    st.markdown("---")
                    st.subheader("📊 Forensic Analysis Report")

                    if "error" in results:
                        st.error(f"⚠️ Analysis failed: {results['error']}")
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            icon = "🔴" if results["is_fake"] else "🟢"
                            verdict_text = f"VERDICT: {icon} {results['verdict']}"
                            if results["is_fake"]:
                                st.error(verdict_text)
                            else:
                                st.success(verdict_text)
                        with col2:
                            st.metric(label="Cloning Confidence", value=results["confidence"], delta=results["risk_level"])

                        if results["is_fake"]:
                            st.info("💡 **Actionable Recommendation:** High risk of voice cloning detected. Do not transfer funds or execute requested actions.")
                        else:
                            st.info("💡 **Actionable Recommendation:** No strong signs of AI voice cloning detected.")