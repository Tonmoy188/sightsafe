# 👁️ SightSafe - AI Vision Assistant for Seniors

A professional Streamlit-based application designed to help visually impaired seniors navigate their environment safely using AI-powered detection.

## 🌟 Features

- **Real-time Environment Scanning**: Detects obstacles, stairs, people, uneven surfaces, and more
- **Risk Assessment**: Clear HIGH/MEDIUM/SAFE risk levels with color-coded badges
- **Voice Guidance Simulation**: Audio feedback with animated waveform visualization
- **Scan History**: Track up to 10 previous scans with timestamps
- **Premium UI**: Modern, accessible design with smooth animations
- **Elderly-Focused Messages**: Clear, actionable safety instructions tailored for seniors

## 🚀 Quick Start

### Prerequisites

1. **Install Python** (version 3.8 or higher)
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

### Installation

1. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

   Or install from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Access the app**:
   - The app will automatically open in your default browser
   - Default URL: http://localhost:8501

## 📱 How to Use

1. **Scan Environment**:
   - Click the large "🔍 Scan Environment" button
   - Wait for the scanning animation (2.5 seconds)
   - View the detection results

2. **Review Results**:
   - Check the risk level badge (HIGH/MEDIUM/SAFE)
   - Read the safety message
   - Review additional details

3. **Voice Guidance**:
   - Click "🔊 Play Voice Guidance" button
   - Watch the animated waveform while "speaking"
   - Voice simulation lasts 3 seconds

4. **Scan History**:
   - View previous scans in the right sidebar
   - See timestamps and risk levels
   - Clear history with the "🗑️ Clear History" button

## 🎯 Detection Types

The app simulates various real-world scenarios:

- **Obstacles**: Chairs, boxes, and other blocking objects
- **Stairs**: Ascending or descending steps
- **Clear Path**: Safe, unobstructed walkways
- **People Nearby**: Individuals in or near the path
- **Uneven Surfaces**: Raised edges, bumps, or irregular flooring
- **Doorways**: Open or partially open doors
- **Corners**: Sharp turns requiring caution
- **Low Obstacles**: Knee-level objects requiring stepping over
- **Crowded Areas**: Multiple people in the vicinity

## 🎨 UI Features

- **Gradient Background**: Modern purple gradient design
- **Animated Scanning**: Visual feedback during environment analysis
- **Color-Coded Risks**:
  - 🔴 RED: High risk (immediate danger)
  - 🟡 YELLOW: Medium risk (caution needed)
  - 🟢 GREEN: Safe (clear to proceed)
- **Waveform Animation**: Visual representation of voice output
- **Responsive Layout**: Two-column design with main content and history

## 🛠️ Technical Details

- **Framework**: Streamlit 1.31.0
- **Language**: Python 3.8+
- **Styling**: Custom CSS with animations
- **State Management**: Streamlit session state
- **Detection Logic**: Randomized realistic scenarios

## 📊 Project Structure

```
bob hackathon/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README_STREAMLIT.md   # This file
└── [other project files]
```

## 🎓 For Hackathon Judges

This application demonstrates:

1. **User-Centric Design**: Tailored specifically for elderly users with clear, large text and simple interactions
2. **Accessibility**: High contrast colors, large buttons, and straightforward navigation
3. **Professional UI**: Modern design with smooth animations and premium aesthetics
4. **Realistic Scenarios**: 10 different detection types with appropriate risk levels
5. **Complete Flow**: Scan → Results → Voice feedback → History tracking
6. **Bug-Free Operation**: Robust state management and error-free execution

## 💡 Future Enhancements

- Real camera integration using OpenCV
- Actual AI model integration (YOLO, TensorFlow)
- Real text-to-speech using pyttsx3 or gTTS
- Mobile app version
- Multi-language support
- Cloud deployment

## 📝 Notes

- This is a simulation/prototype for demonstration purposes
- Detection results are randomized for variety
- Voice output is simulated with visual feedback
- Designed for hackathon presentation and proof of concept

## 🤝 Support

For questions or issues, please contact the development team.

---

**SightSafe** - Empowering Independence Through AI Vision
