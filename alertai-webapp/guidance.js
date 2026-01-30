// AlertAI Guidance Agent JavaScript
class GuidanceAgent {
    constructor() {
        this.isListening = false;
        this.isSpeaking = false;
        this.isMuted = false;
        this.useKeyboard = false;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.currentVoice = null;
        this.conversationHistory = []; // For API communication
        this.emergencyType = 'Fire'; // Default, will be set from URL params
        this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
        this.speechPermissionGranted = false;
        this.pendingInitialMessage = null; // Store initial message for iOS
        this.autoListenEnabled = true; // Enable auto-listening after TTS
        this.isUserInitiatedListening = false; // Track if listening was started by user or auto
        
        this.init();
    }

    init() {
        this.setupEmergencyInfo();
        this.setupSpeechSynthesis();
        this.setupSpeechRecognition();
        this.setupEventListeners();
        this.hideLoading();
        
        // Check for iOS and request speech permission
        if (this.isIOS) {
            this.handleIOSSpeech();
        } else {
            this.initializeSpeech();
        }
        
        // Start with initial agent message from real agent
        setTimeout(() => {
            // Create appropriate initial message based on emergency type
            const initialMessages = {
                'Fire': "FIRE EMERGENCY detected! Start step-by-step fire safety guidance immediately.",
                'Blood': "BLOOD EMERGENCY detected! Start step-by-step trauma response guidance immediately.",
                'Smoke': "SMOKE EMERGENCY detected! Start step-by-step smoke safety guidance immediately.",
                'Fallen Person': "FALLEN PERSON EMERGENCY detected! Start step-by-step medical response guidance immediately.",
                'Gun': "SECURITY EMERGENCY detected! Start step-by-step security response guidance immediately."
            };
            
            const initialMessage = initialMessages[this.emergencyType] || initialMessages['Fire'];
            
            // On iOS, don't auto-speak until user grants permission
            if (this.isIOS && !this.speechPermissionGranted) {
                console.log('iOS detected - waiting for speech permission before initial message');
                // Store the initial message to speak later
                this.pendingInitialMessage = initialMessage;
            } else {
                this.callRealAgent(initialMessage);
            }
        }, 1000);
    }

    setupEmergencyInfo() {
        // Get emergency type from URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const newEmergencyType = urlParams.get('type') || 'Fire';
        
        // CRITICAL FIX: Clear conversation history when emergency type changes
        if (this.emergencyType !== newEmergencyType) {
            console.log(`Emergency type changed from ${this.emergencyType} to ${newEmergencyType} - clearing conversation history`);
            this.conversationHistory = []; // Clear history to prevent agent contamination
            this.clearHistoryDisplay(); // Clear UI display as well
        }
        
        this.emergencyType = newEmergencyType;
        
        // Update UI based on emergency type
        const emergencyConfig = {
            'Fire': {
                title: 'Fire Safety Agent',
                icon: 'fas fa-fire',
                color: '#e74c3c'
            },
            'Blood': {
                title: 'Trauma Response Agent',
                icon: 'fas fa-tint',
                color: '#c0392b'
            },
            'Smoke': {
                title: 'Smoke Safety Agent',
                icon: 'fas fa-smog',
                color: '#95a5a6'
            },
            'Fallen Person': {
                title: 'Medical Response Agent',
                icon: 'fas fa-user-injured',
                color: '#f39c12'
            },
            'Gun': {
                title: 'Security Response Agent',
                icon: 'fas fa-exclamation-circle',
                color: '#8e44ad'
            }
        };

        const config = emergencyConfig[this.emergencyType] || emergencyConfig['Fire'];
        
        document.getElementById('emergencyTitle').textContent = config.title;
        document.getElementById('emergencyIcon').innerHTML = `<i class="${config.icon}"></i>`;
        document.getElementById('emergencyIcon').style.borderColor = config.color;
        document.querySelector('.emergency-icon i').style.color = config.color;
    }

    setupSpeechSynthesis() {
        // Wait for voices to load
        if (this.synthesis.getVoices().length === 0) {
            this.synthesis.addEventListener('voiceschanged', () => {
                this.selectBestVoice();
            });
        } else {
            this.selectBestVoice();
        }
    }

    selectBestVoice() {
        const voices = this.synthesis.getVoices();
        
        // Prefer English voices, then system default
        const preferredVoices = [
            'Google US English',
            'Microsoft Zira - English (United States)',
            'Alex',
            'Samantha',
            'Karen'
        ];

        for (const voiceName of preferredVoices) {
            const voice = voices.find(v => v.name.includes(voiceName));
            if (voice) {
                this.currentVoice = voice;
                return;
            }
        }

        // Fallback to first English voice
        this.currentVoice = voices.find(v => v.lang.startsWith('en')) || voices[0];
    }

    setupSpeechRecognition() {
        // Check for speech recognition support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech recognition not supported');
            this.showKeyboardInput();
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateSpeechButton('listening');
            this.updateStatusIndicator('speechStatus2', 'Listening...', 'active');
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.handleUserInput(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.isUserInitiatedListening = false; // Reset flag on error
            this.updateSpeechButton('ready');
            
            if (event.error === 'not-allowed' || event.error === 'permission-denied') {
                this.handleSpeechPermissionDenied();
            } else {
                this.updateStatusIndicator('speechStatus2', 'Speech Error', 'error');
                setTimeout(() => {
                    this.updateStatusIndicator('speechStatus2', 'Speech Ready', '');
                }, 3000);
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.isUserInitiatedListening = false; // Reset flag when listening ends
            this.updateSpeechButton('ready');
            this.updateStatusIndicator('speechStatus2', 'Speech Ready', '');
        };
    }

    setupEventListeners() {
        // Text input enter key
        document.getElementById('textInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendTextResponse();
            }
        });

        // Prevent accidental page refresh/back
        window.addEventListener('beforeunload', (e) => {
            e.preventDefault();
            return '';
        });
    }

    // iOS Speech Handling
    handleIOSSpeech() {
        document.getElementById('iosModal').style.display = 'flex';
    }

    requestIOSSpeech() {
        document.getElementById('iosModal').style.display = 'none';
        
        // Set permission granted immediately since user clicked
        this.speechPermissionGranted = true;
        console.log('iOS speech permission granted');
        
        // iOS requires user interaction to request speech permission
        if (this.recognition) {
            this.recognition.start();
            // The permission request will happen automatically
            setTimeout(() => {
                if (this.isListening) {
                    this.recognition.stop();
                }
                this.initializeSpeech();
            }, 1000);
        } else {
            // Even without speech recognition, we can enable speech synthesis
            this.useKeyboardOnly();
            this.initializeSpeech();
        }
        
        // Test speech synthesis with user interaction
        const testUtterance = new SpeechSynthesisUtterance("Speech enabled");
        testUtterance.volume = 0.3; // Audible test
        testUtterance.onend = () => {
            console.log('Test speech completed - now ready for agent responses');
        };
        this.synthesis.speak(testUtterance);
        
        console.log('iOS speech permission requested and granted');
    }

    useKeyboardOnly() {
        document.getElementById('iosModal').style.display = 'none';
        this.speechPermissionGranted = true; // Allow TTS even in keyboard mode
        this.showKeyboardInput();
        this.updateStatusIndicator('speechStatus2', 'Keyboard Mode', '');
        this.initializeSpeech(); // This will trigger pending initial message
    }

    initializeSpeech() {
        this.updateStatusIndicator('speechStatus2', 'Speech Ready', '');
        console.log('initializeSpeech called, speechPermissionGranted:', this.speechPermissionGranted);
        
        // If there's a pending initial message (iOS), send it now
        if (this.pendingInitialMessage) {
            console.log('Sending pending initial message for iOS:', this.pendingInitialMessage);
            this.callRealAgent(this.pendingInitialMessage);
            this.pendingInitialMessage = null;
        }
    }

    handleSpeechPermissionDenied() {
        this.showKeyboardInput();
        this.updateStatusIndicator('speechStatus2', 'Permission Denied', 'error');
        
        // Show helpful message
        setTimeout(() => {
            alert('Microphone access was denied. You can still use the keyboard input or refresh the page to try again.');
        }, 500);
    }

    // Speech Recognition Control
    toggleSpeechRecognition() {
        // Check if button is disabled (during processing or speaking)
        const button = document.getElementById('speechBtn');
        if (button.disabled) {
            console.log('Speech button is disabled, ignoring click');
            return;
        }
        
        if (!this.recognition) {
            this.showKeyboardInput();
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            if (this.isSpeaking) {
                this.synthesis.cancel();
                this.stopSpeaking();
            }
            
            // Mark this as user-initiated listening
            this.isUserInitiatedListening = true;
            
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Failed to start speech recognition:', error);
                this.isUserInitiatedListening = false; // Reset flag on error
                this.handleSpeechPermissionDenied();
            }
        }
    }

    updateSpeechButton(state) {
        const button = document.getElementById('speechBtn');
        const status = document.getElementById('speechStatus');
        
        button.className = 'speech-btn';
        
        switch (state) {
            case 'listening':
                button.classList.add('listening');
                // Show different text based on whether this was auto-started or user-initiated
                const listeningText = this.autoListenEnabled && !this.isUserInitiatedListening ? 'Tap to Stop' : 'Listening...';
                button.innerHTML = `<i class="fas fa-microphone"></i><span class="speech-status">${listeningText}</span>`;
                button.disabled = false;
                break;
            case 'processing':
                button.classList.add('processing');
                button.innerHTML = '<i class="fas fa-cog fa-spin"></i><span class="speech-status">Processing...</span>';
                button.disabled = true; // Disable during processing
                break;
            case 'speaking':
                button.classList.add('speaking');
                button.innerHTML = '<i class="fas fa-volume-up"></i><span class="speech-status">Speaking...</span>';
                button.disabled = true; // Disable while speaking
                break;
            case 'ready':
            default:
                button.innerHTML = '<i class="fas fa-microphone"></i><span class="speech-status">Tap to Speak</span>';
                button.disabled = false; // Enable for user input
                break;
        }
    }

    // Text Input Control
    toggleInputMethod() {
        this.useKeyboard = !this.useKeyboard;
        const textContainer = document.getElementById('textInputContainer');
        const speechControls = document.querySelector('.speech-controls');
        const toggleBtn = document.querySelector('.toggle-input-btn');
        
        if (this.useKeyboard) {
            textContainer.style.display = 'flex';
            speechControls.style.display = 'none';
            toggleBtn.innerHTML = '<i class="fas fa-microphone"></i> Use Voice';
            document.getElementById('textInput').focus();
        } else {
            textContainer.style.display = 'none';
            speechControls.style.display = 'flex';
            toggleBtn.innerHTML = '<i class="fas fa-keyboard"></i> Use Keyboard';
        }
    }

    showKeyboardInput() {
        this.useKeyboard = true;
        this.toggleInputMethod();
    }

    sendTextResponse() {
        const input = document.getElementById('textInput');
        const text = input.value.trim();
        
        if (text) {
            this.handleUserInput(text);
            input.value = '';
        }
    }

    // User Input Processing
    handleUserInput(text) {
        console.log('User input:', text);
        
        // Add to conversation history
        this.addToHistory('user', text);
        
        // Update speech button to processing
        this.updateSpeechButton('processing');
        
        // Call the real Python agent via API
        this.callRealAgent(text);
    }

    async callRealAgent(userMessage) {
        try {
            // Show processing state
            document.getElementById('responseText').textContent = 'Processing your request...';
            
            const response = await fetch('/api/guidance-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    emergency_type: this.emergencyType,
                    message: userMessage,
                    history: this.conversationHistory
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update conversation history
                this.conversationHistory = data.conversation_history || this.conversationHistory;
                
                // Process the real agent response
                this.processRealAgentResponse(data.response, data.agent_type);
            } else {
                // Handle error - but still use real agent response, don't fall back to mock
                const errorResponse = data.response || "I'm experiencing technical difficulties. Please call emergency services at 911.";
                this.processRealAgentResponse(errorResponse, "Emergency Agent");
            }
            
        } catch (error) {
            console.error('Error calling real agent:', error);
            
            // Instead of falling back to mock, show a proper error message
            console.log('API call failed - showing error message instead of mock response');
            const errorMessage = "🚨 I'm experiencing connection issues with the emergency guidance system. Please call 911 immediately for emergency assistance. If safe to do so, try refreshing the page.";
            this.processRealAgentResponse(errorMessage, "Emergency System");
        }
    }

    processRealAgentResponse(response, agentType) {
        console.log('processRealAgentResponse called');
        console.log('Real agent response:', response);
        console.log('Agent type:', agentType);
        
        // Add to conversation history
        this.addToHistory('agent', response);
        
        // Check if response mentions CPR and show button if needed
        this.checkForCPRRecommendation(response);
        
        // Speak the response (this will handle the speech button state)
        console.log('About to call speakResponse');
        this.speakResponse(response);
        
        // Don't reset speech button here - let TTS finish first
        // The speech button will be reset in stopSpeaking() when TTS finishes
        
        // Update agent type display if provided
        if (agentType) {
            document.getElementById('emergencyTitle').textContent = agentType;
        }
    }

    processAgentResponse(userInput) {
        // Fallback mock responses (kept for offline mode)
        let response = this.generateMockResponse(userInput);
        
        // Add to conversation history
        this.addToHistory('agent', response);
        
        // Speak the response (this will handle the speech button state)
        this.speakResponse(response);
        
        // Don't reset speech button here - let TTS finish first
        // The speech button will be reset in stopSpeaking() when TTS finishes
    }

    generateMockResponse(userInput) {
        const input = userInput.toLowerCase();
        
        // Simple response logic for demo
        if (input.includes('first floor') || input.includes('1st floor')) {
            return "I understand you're on the 1st floor. Can you see any smoke or fire from your current location? Please describe what you observe.";
        } else if (input.includes('ground floor') || input.includes('lobby')) {
            return "You're on the ground floor. Look for the nearest fire extinguisher near the main entrance. Can you see it?";
        } else if (input.includes('yes') || input.includes('can see')) {
            return "Good. Now, assess the size of the fire. Is it smaller than a wastepaper basket, or larger? This will determine our next step.";
        } else if (input.includes('no') || input.includes('cannot see')) {
            return "That's good news. Proceed to the nearest emergency exit. Do you know where the closest exit is from your location?";
        } else if (input.includes('small') || input.includes('little')) {
            return "For a small fire, you may attempt to extinguish it. Get the ABC fire extinguisher and remember PASS: Pull, Aim, Squeeze, Sweep. Are you trained in fire extinguisher use?";
        } else if (input.includes('large') || input.includes('big')) {
            return "For a large fire, do NOT attempt to fight it. Evacuate immediately using the nearest exit. Call 911 if you haven't already. Confirm when you're moving to safety.";
        } else {
            return "I understand. Let me help you with the next step. Can you tell me more about your current situation and what you can see around you?";
        }
    }

    // Text-to-Speech
    speakResponse(text) {
        console.log('speakResponse called with:', text);
        console.log('isMuted:', this.isMuted);
        console.log('synthesis available:', !!this.synthesis);
        console.log('isIOS:', this.isIOS);
        
        if (this.isMuted) {
            console.log('Speech blocked: muted');
            return;
        }
        
        // On iOS, speech might be blocked until user interaction
        if (this.isIOS && !this.speechPermissionGranted) {
            console.log('iOS speech blocked - no permission yet, updating text only');
            // Still update the text display
            document.getElementById('responseText').textContent = text;
            return;
        }
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        if (this.currentVoice) {
            utterance.voice = this.currentVoice;
            console.log('Using voice:', this.currentVoice.name);
        } else {
            console.log('No voice selected, using default');
        }
        
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        utterance.onstart = () => {
            console.log('Speech started');
            this.startSpeaking();
        };
        
        utterance.onend = () => {
            console.log('Speech ended');
            this.stopSpeaking();
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            console.log('Error details:', event.error);
            this.stopSpeaking();
            
            // On iOS, if speech fails, show a message
            if (this.isIOS) {
                console.log('iOS speech failed - might need user interaction');
            }
        };
        
        // Update response text
        document.getElementById('responseText').textContent = text;
        
        // Speak
        console.log('Calling synthesis.speak()');
        this.synthesis.speak(utterance);
    }

    startSpeaking() {
        this.isSpeaking = true;
        document.getElementById('agentAvatar').classList.add('speaking');
        // Set speech button to speaking state
        this.updateSpeechButton('speaking');
    }

    stopSpeaking() {
        this.isSpeaking = false;
        document.getElementById('agentAvatar').classList.remove('speaking');
        
        // Auto-start listening after TTS finishes (seamless conversation)
        if (this.autoListenEnabled) {
            setTimeout(() => {
                // Only auto-start if speech recognition is available and conditions are met
                if (this.recognition && !this.isMuted && !this.isListening && 
                    (!this.isIOS || this.speechPermissionGranted)) {
                    console.log('Auto-starting speech recognition after TTS finished');
                    
                    // Mark this as auto-initiated listening (not user-initiated)
                    this.isUserInitiatedListening = false;
                    
                    try {
                        this.recognition.start();
                        // The recognition.onstart event will handle the button state
                    } catch (error) {
                        console.error('Failed to auto-start speech recognition:', error);
                        // Fallback to ready state if auto-start fails
                        this.updateSpeechButton('ready');
                    }
                } else {
                    // If speech recognition not available or conditions not met, just set to ready
                    this.updateSpeechButton('ready');
                }
            }, 500); // Small delay to ensure TTS has fully stopped
        } else {
            // Auto-listen disabled, just set to ready
            this.updateSpeechButton('ready');
        }
    }

    // Conversation History
    addToHistory(sender, message) {
        this.conversationHistory.push({ sender, message, timestamp: new Date() });
        this.updateHistoryDisplay();
    }

    updateHistoryDisplay() {
        const historyContent = document.getElementById('historyContent');
        
        historyContent.innerHTML = this.conversationHistory
            .slice(-10) // Show last 10 messages
            .map(item => `
                <div class="history-message ${item.sender}">
                    <strong>${item.sender === 'user' ? 'You' : 'Agent'}:</strong>
                    ${item.message}
                </div>
            `).join('');
        
        // Auto-scroll to bottom
        historyContent.scrollTop = historyContent.scrollHeight;
    }

    clearHistoryDisplay() {
        const historyContent = document.getElementById('historyContent');
        if (historyContent) {
            historyContent.innerHTML = '<div class="history-message system"><strong>System:</strong> Conversation history cleared for new emergency type</div>';
        }
    }

    toggleHistory() {
        const history = document.getElementById('conversationHistory');
        history.classList.toggle('expanded');
    }

    // Control Functions
    toggleMute() {
        this.isMuted = !this.isMuted;
        const muteBtn = document.getElementById('muteBtn');
        
        if (this.isMuted) {
            muteBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
            this.synthesis.cancel();
            this.stopSpeaking();
        } else {
            muteBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
        }
    }

    toggleAutoListen() {
        this.autoListenEnabled = !this.autoListenEnabled;
        const toggleBtn = document.getElementById('autoListenToggle');
        
        if (this.autoListenEnabled) {
            toggleBtn.innerHTML = '<i class="fas fa-magic"></i> Auto-Listen: ON';
            toggleBtn.classList.remove('disabled');
        } else {
            toggleBtn.innerHTML = '<i class="fas fa-magic"></i> Auto-Listen: OFF';
            toggleBtn.classList.add('disabled');
        }
        
        console.log('Auto-listen toggled:', this.autoListenEnabled);
    }

    // CPR Monitor Integration
    showCPRMonitorButton() {
        const cprBtn = document.getElementById('cprMonitorBtn');
        if (cprBtn) {
            cprBtn.style.display = 'flex';
            console.log('CPR Monitor button shown');
        }
    }

    hideCPRMonitorButton() {
        const cprBtn = document.getElementById('cprMonitorBtn');
        if (cprBtn) {
            cprBtn.style.display = 'none';
            console.log('CPR Monitor button hidden');
        }
    }

    launchCPRMonitor() {
        console.log('Launching CPR Monitor...');
        
        // Open CPR monitor in new window/tab
        const cprWindow = window.open('/cpr-monitor', 'cpr-monitor', 'width=1200,height=800,scrollbars=yes,resizable=yes');
        
        if (cprWindow) {
            // Focus the new window
            cprWindow.focus();
            
            // Provide voice feedback
            this.speak("CPR Monitor launched. Follow the visual guides and listen for the beep rhythm. Push hard and fast on the center of the chest.", true);
            
            console.log('CPR Monitor launched successfully');
        } else {
            // Fallback if popup blocked
            console.warn('Popup blocked, redirecting to CPR monitor');
            window.location.href = '/cpr-monitor';
        }
    }

    // Check if agent response mentions CPR and show button accordingly
    checkForCPRRecommendation(response) {
        const cprKeywords = [
            'cpr', 'chest compressions', 'cardiopulmonary resuscitation',
            'not breathing', 'no pulse', 'unconscious', 'cardiac arrest',
            'heart stopped', 'compressions', 'rescue breathing'
        ];
        
        const responseText = response.toLowerCase();
        const containsCPRKeywords = cprKeywords.some(keyword => responseText.includes(keyword));
        
        if (containsCPRKeywords) {
            console.log('CPR keywords detected in agent response');
            this.showCPRMonitorButton();
        }
        
        return containsCPRKeywords;
    }

    exitGuidance() {
        if (confirm('Are you sure you want to exit the guidance session?')) {
            this.synthesis.cancel();
            if (this.recognition && this.isListening) {
                this.recognition.stop();
            }
            
            // Return to main app or close
            if (window.opener) {
                window.close();
            } else {
                window.location.href = 'alertai.html';
            }
        }
    }

    updateStatusIndicator(id, text, className) {
        const indicator = document.getElementById(id);
        if (indicator) {
            indicator.querySelector('span').textContent = text;
            indicator.className = 'status-item ' + (className || '');
        }
    }

    hideLoading() {
        setTimeout(() => {
            document.getElementById('loadingOverlay').style.display = 'none';
        }, 2000);
    }
}

// Global functions for HTML onclick events
function toggleSpeechRecognition() {
    window.guidanceAgent.toggleSpeechRecognition();
}

function sendTextResponse() {
    window.guidanceAgent.sendTextResponse();
}

function toggleInputMethod() {
    window.guidanceAgent.toggleInputMethod();
}

function toggleHistory() {
    window.guidanceAgent.toggleHistory();
}

function toggleMute() {
    window.guidanceAgent.toggleMute();
}

function exitGuidance() {
    window.guidanceAgent.exitGuidance();
}

function requestIOSSpeech() {
    window.guidanceAgent.requestIOSSpeech();
}

function useKeyboardOnly() {
    window.guidanceAgent.useKeyboardOnly();
}

function toggleAutoListen() {
    window.guidanceAgent.toggleAutoListen();
}

function launchCPRMonitor() {
    window.guidanceAgent.launchCPRMonitor();
}

// Initialize the guidance agent when page loads
window.addEventListener('DOMContentLoaded', () => {
    window.guidanceAgent = new GuidanceAgent();
});

// Handle page visibility changes (pause speech when tab is hidden)
document.addEventListener('visibilitychange', () => {
    if (document.hidden && window.guidanceAgent) {
        window.guidanceAgent.synthesis.cancel();
        window.guidanceAgent.stopSpeaking();
    }
});