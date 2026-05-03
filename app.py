import streamlit as st
import time
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SightSafe - AI Vision Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Card styling */
    .stApp {
        background: transparent;
    }
    
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Header styling */
    h1 {
        color: #2d3748;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 3rem !important;
    }
    
    h2 {
        color: #4a5568;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    h3 {
        color: #2d3748;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px;
        font-weight: 700;
        border-radius: 15px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Risk badge styling */
    .risk-badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 18px;
        margin: 1rem 0;
    }
    
    .risk-high {
        background: #fee;
        color: #c53030;
        border: 2px solid #fc8181;
    }
    
    .risk-medium {
        background: #fef5e7;
        color: #d97706;
        border: 2px solid #fbbf24;
    }
    
    .risk-safe {
        background: #f0fdf4;
        color: #15803d;
        border: 2px solid #4ade80;
    }
    
    /* Camera simulation area */
    .camera-sim {
        background: #1a202c;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .camera-placeholder {
        color: #a0aec0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Scanning animation */
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(300%); }
    }
    
    .scanning-line {
        position: absolute;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        animation: scan 2s linear infinite;
        box-shadow: 0 0 20px #667eea;
    }
    
    /* Voice animation */
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .voice-active {
        animation: pulse 1s ease-in-out infinite;
    }
    
    /* Waveform animation */
    @keyframes wave {
        0%, 100% { height: 20px; }
        50% { height: 60px; }
    }
    
    .waveform {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
        margin: 1rem 0;
    }
    
    .wave-bar {
        width: 4px;
        background: #667eea;
        border-radius: 2px;
        animation: wave 0.8s ease-in-out infinite;
    }
    
    .wave-bar:nth-child(2) { animation-delay: 0.1s; }
    .wave-bar:nth-child(3) { animation-delay: 0.2s; }
    .wave-bar:nth-child(4) { animation-delay: 0.3s; }
    .wave-bar:nth-child(5) { animation-delay: 0.4s; }
    
    /* History card */
    .history-card {
        background: #f7fafc;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    /* Info box */
    .info-box {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'is_scanning' not in st.session_state:
    st.session_state.is_scanning = False
if 'is_speaking' not in st.session_state:
    st.session_state.is_speaking = False

# Detection scenarios with realistic messages for elderly users
DETECTION_SCENARIOS = [
    {
        'type': 'obstacle',
        'risk': 'HIGH',
        'message': 'CAUTION: Large obstacle detected 3 feet ahead. Please stop and carefully navigate around it to your left.',
        'details': 'A chair is blocking your path. Take small steps to the left to go around it safely.'
    },
    {
        'type': 'stairs',
        'risk': 'HIGH',
        'message': 'WARNING: Stairs detected directly ahead. Stop immediately and use the handrail.',
        'details': 'There are 8 steps going down. Please hold the railing firmly with both hands before descending.'
    },
    {
        'type': 'clear_path',
        'risk': 'SAFE',
        'message': 'Path is clear ahead. You may proceed forward safely at a comfortable pace.',
        'details': 'No obstacles detected for the next 10 feet. The floor is level and even.'
    },
    {
        'type': 'person_nearby',
        'risk': 'MEDIUM',
        'message': 'NOTICE: Person detected 5 feet ahead on your right side. Please slow down.',
        'details': 'Someone is standing near your path. They appear to be stationary. Proceed with caution.'
    },
    {
        'type': 'uneven_surface',
        'risk': 'HIGH',
        'message': 'ALERT: Uneven floor surface ahead. Step carefully and watch your footing.',
        'details': 'The floor has a raised edge about 2 inches high. Lift your feet higher when stepping forward.'
    },
    {
        'type': 'doorway',
        'risk': 'MEDIUM',
        'message': 'Doorway detected ahead. The door is partially open. Proceed slowly.',
        'details': 'Door opening is 2 feet wide. You may need to push it further open to pass through comfortably.'
    },
    {
        'type': 'clear_path',
        'risk': 'SAFE',
        'message': 'All clear! The hallway ahead is empty and well-lit. Safe to continue walking.',
        'details': 'Straight path for 15 feet with good lighting. No obstacles or hazards detected.'
    },
    {
        'type': 'low_obstacle',
        'risk': 'MEDIUM',
        'message': 'CAUTION: Low object detected at knee level, 4 feet ahead. Please step over carefully.',
        'details': 'A small box or bag is on the floor. Lift your foot about 6 inches to step over it.'
    },
    {
        'type': 'corner',
        'risk': 'MEDIUM',
        'message': 'Sharp corner ahead on your left. Please slow down and turn carefully.',
        'details': 'Wall corner at 90 degrees. Keep your right hand extended to feel the wall as you turn.'
    },
    {
        'type': 'multiple_people',
        'risk': 'HIGH',
        'message': 'NOTICE: Multiple people detected ahead. Area is crowded. Please wait or proceed very slowly.',
        'details': 'At least 3 people are in your path. Consider waiting for them to pass or ask for assistance.'
    }
]

def perform_scan():
    """Simulate environment scanning with realistic detection"""
    # Random selection from scenarios
    scenario = random.choice(DETECTION_SCENARIOS)
    
    return {
        'timestamp': datetime.now().strftime('%I:%M %p'),
        'type': scenario['type'],
        'risk': scenario['risk'],
        'message': scenario['message'],
        'details': scenario['details']
    }

def get_risk_color(risk_level):
    """Return color class based on risk level"""
    colors = {
        'HIGH': 'risk-high',
        'MEDIUM': 'risk-medium',
        'SAFE': 'risk-safe'
    }
    return colors.get(risk_level, 'risk-medium')

# App Header
st.markdown("<h1>👁️ SightSafe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #718096; font-size: 1.2rem; margin-bottom: 2rem;'>AI-Powered Vision Assistant for Seniors</p>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📸 Environment Scanner")
    
    # Camera simulation area
    if st.session_state.is_scanning:
        st.markdown("""
        <div class="camera-sim">
            <div class="scanning-line"></div>
            <div class="camera-placeholder">🔍 Scanning Environment...</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate scanning delay
        time.sleep(2.5)
        
        # Perform scan
        result = perform_scan()
        st.session_state.current_result = result
        st.session_state.scan_history.insert(0, result)
        
        # Keep only last 10 scans
        if len(st.session_state.scan_history) > 10:
            st.session_state.scan_history = st.session_state.scan_history[:10]
        
        st.session_state.is_scanning = False
        st.rerun()
    else:
        st.markdown("""
        <div class="camera-sim">
            <div class="camera-placeholder">📷 Ready to Scan</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Scan button
    if st.button("🔍 Scan Environment", key="scan_btn", disabled=st.session_state.is_scanning):
        st.session_state.is_scanning = True
        st.rerun()
    
    # Display current result
    if st.session_state.current_result:
        st.markdown("---")
        st.markdown("### 📊 Detection Results")
        
        result = st.session_state.current_result
        risk_class = get_risk_color(result['risk'])
        
        # Risk badge
        st.markdown(f"""
        <div class="risk-badge {risk_class}">
            ⚠️ Risk Level: {result['risk']}
        </div>
        """, unsafe_allow_html=True)
        
        # Detection type
        st.markdown(f"**Detection Type:** {result['type'].replace('_', ' ').title()}")
        
        # Safety message
        st.markdown("#### 💬 Safety Message")
        st.info(result['message'])
        
        # Additional details
        st.markdown("#### 📝 Details")
        st.markdown(f"<div class='info-box'>{result['details']}</div>", unsafe_allow_html=True)
        
        # Voice simulation button
        st.markdown("---")
        
        if st.session_state.is_speaking:
            st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <div class='voice-active' style='font-size: 2rem; margin-bottom: 1rem;'>🔊</div>
                <div style='font-size: 1.5rem; font-weight: 600; color: #667eea; margin-bottom: 1rem;'>Speaking...</div>
                <div class='waveform'>
                    <div class='wave-bar' style='height: 30px;'></div>
                    <div class='wave-bar' style='height: 45px;'></div>
                    <div class='wave-bar' style='height: 60px;'></div>
                    <div class='wave-bar' style='height: 45px;'></div>
                    <div class='wave-bar' style='height: 30px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate speaking duration
            time.sleep(3)
            st.session_state.is_speaking = False
            st.rerun()
        else:
            if st.button("🔊 Play Voice Guidance", key="voice_btn", use_container_width=True):
                st.session_state.is_speaking = True
                st.rerun()

with col2:
    st.markdown("### 📜 Scan History")
    
    if st.session_state.scan_history:
        for idx, scan in enumerate(st.session_state.scan_history):
            risk_class = get_risk_color(scan['risk'])
            
            st.markdown(f"""
            <div class="history-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600; color: #2d3748;">#{idx + 1}</span>
                    <span style="color: #718096; font-size: 0.9rem;">{scan['timestamp']}</span>
                </div>
                <div class="risk-badge {risk_class}" style="font-size: 0.9rem; padding: 6px 12px;">
                    {scan['risk']}
                </div>
                <div style="margin-top: 0.5rem; color: #4a5568; font-size: 0.95rem;">
                    {scan['type'].replace('_', ' ').title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; color: #a0aec0;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📭</div>
            <div>No scans yet</div>
            <div style='font-size: 0.9rem; margin-top: 0.5rem;'>Start scanning to see history</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Clear history button
    if st.session_state.scan_history:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.scan_history = []
            st.session_state.current_result = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #a0aec0; padding: 1rem;'>
    <p style='margin: 0;'>SightSafe - Empowering Independence Through AI Vision</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Designed for visually impaired seniors</p>
</div>
""", unsafe_allow_html=True)

# Made with Bob
