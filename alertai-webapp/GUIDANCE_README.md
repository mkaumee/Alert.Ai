# 🤖 AlertAI Guidance Agent Interface

A beautiful, full-screen voice-enabled guidance interface for emergency response with specialized AI agents.

## ✨ Features

### 🎤 **Speech-to-Text & Text-to-Speech**
- **Voice Input**: Tap-to-speak with visual feedback
- **Voice Output**: Agent responses with natural speech
- **iOS Compatibility**: Proper handling of iOS speech restrictions
- **Fallback Support**: Keyboard input when speech is unavailable

### 🎨 **Beautiful UI/UX**
- **Full-Screen Interface**: Immersive emergency guidance experience
- **Glowing Avatar**: Visual indicator when agent is speaking
- **Responsive Design**: Works perfectly on mobile and desktop
- **Emergency-Themed**: Color-coded for different emergency types

### 🚨 **Emergency-Specific Agents**
- **Fire Safety Agent**: Fire suppression and evacuation guidance
- **Trauma Response Agent**: Bleeding control and medical response
- **Smoke Safety Agent**: Smoke evacuation and breathing safety
- **Medical Response Agent**: First aid and injury assessment
- **Security Response Agent**: Lockdown and threat response

## 🚀 How to Use

### 1. **From Main AlertAI App**
```javascript
// Emergency alert appears → Click "Start Guidance Agent"
// Opens guidance.html with emergency type parameter
```

### 2. **Direct Testing**
```bash
# Open test page
open alertai-webapp/test_guidance.html

# Or open specific agent directly
open alertai-webapp/guidance.html?type=Fire&building=Test&floor=1st
```

### 3. **URL Parameters**
```
guidance.html?type=Fire&building=Medical Center&floor=1st Floor
```

## 📱 iOS Speech Compatibility

### **The Problem**
iOS Safari requires explicit user interaction for speech permissions and has restrictions on when speech recognition can be activated.

### **Our Solution**
```javascript
// 1. Detect iOS
this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

// 2. Show permission modal on iOS
if (this.isIOS) {
    this.handleIOSSpeech(); // Shows modal
}

// 3. Request permission with user interaction
requestIOSSpeech() {
    // User taps "Enable Voice" button
    this.recognition.start(); // This works because it's user-initiated
}

// 4. Fallback to keyboard
useKeyboardOnly() {
    this.showKeyboardInput(); // Always available
}
```

## 🎯 Technical Implementation

### **Speech Recognition**
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
this.recognition = new SpeechRecognition();
this.recognition.continuous = false;
this.recognition.interimResults = false;
this.recognition.lang = 'en-US';
```

### **Speech Synthesis**
```javascript
this.synthesis = window.speechSynthesis;
const utterance = new SpeechSynthesisUtterance(text);
utterance.voice = this.currentVoice; // Best English voice
utterance.rate = 0.9; // Slightly slower for clarity
```

### **Visual Speaking Indicator**
```css
.agent-avatar.speaking .glow-ring {
    opacity: 1;
    transform: scale(1.2);
    animation: speaking-glow 1.5s ease-in-out infinite;
}

.agent-avatar.speaking .avatar-inner {
    animation: speaking-bounce 0.8s ease-in-out infinite;
}
```

## 🎨 Styling Features

### **Responsive Design**
- Desktop: Full layout with side panels
- Mobile: Stacked layout, larger touch targets
- Tablet: Optimized for touch interaction

### **Accessibility**
- High contrast mode support
- Reduced motion for accessibility
- Keyboard navigation
- Screen reader friendly

### **Emergency Color Coding**
```javascript
const emergencyConfig = {
    'Fire': { color: '#e74c3c', icon: 'fas fa-fire' },
    'Blood': { color: '#c0392b', icon: 'fas fa-tint' },
    'Smoke': { color: '#95a5a6', icon: 'fas fa-smog' },
    // ... etc
};
```

## 🔧 Files Structure

```
alertai-webapp/
├── guidance.html          # Main guidance interface
├── guidance.css           # Full-screen styling with animations
├── guidance.js            # Speech & interaction logic
├── test_guidance.html     # Test page for all agents
└── GUIDANCE_README.md     # This documentation
```

## 🧪 Testing

### **Test All Emergency Types**
```bash
# Open test page
open alertai-webapp/test_guidance.html
```

### **Test Specific Emergency**
```bash
# Fire emergency
open "alertai-webapp/guidance.html?type=Fire"

# Blood emergency  
open "alertai-webapp/guidance.html?type=Blood"

# Test iOS compatibility on iPhone/iPad
```

### **Test Speech Features**
1. **Voice Input**: Tap microphone, speak clearly
2. **Voice Output**: Listen to agent responses
3. **iOS Mode**: Test permission modal on iOS
4. **Keyboard Fallback**: Toggle input method

## 🚀 Integration with Python Agents

The web interface is designed to work alongside the Python emergency agents:

```bash
# Web interface provides beautiful UI
open guidance.html?type=Fire

# Python agent provides AI logic
python alertai-agent/fire_emergency_agent.py
```

**Future Enhancement**: Direct WebSocket connection between web interface and Python agents for real-time communication.

## 🎯 Perfect Emergency Response Experience

1. **Emergency Detected** → AlertAI server processes
2. **Alert Sent** → Web app shows emergency modal  
3. **User Clicks "Start Guidance Agent"** → Opens beautiful guidance interface
4. **Voice Interaction** → Natural conversation with AI agent
5. **Step-by-Step Guidance** → Expert emergency response assistance
6. **Visual Feedback** → Glowing avatar and status indicators
7. **Emergency Resolved** → Complete guidance session

**The AlertAI Guidance Interface provides a professional, accessible, and beautiful emergency response experience! 🚨✨**