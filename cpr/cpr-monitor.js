/**
 * CPR Pose Detection Monitor - Minimal Model for Decentralized AI Network
 * Input: Video stream from camera
 * Output: CPR compression metrics and visual feedback
 */

console.log('[CPR Monitor] Loading minimal pose detection model...');

// State
let bottomSheet = null;
let isFullscreen = false;
let dragHandle = null;
let isDragging = false;
let startY = 0;
let currentY = 0;

// Camera state
let stream = null;
let videoEl = null;
let overlay = null;
let ctx = null;
let cameraActive = false;

// Computer Vision state
let detector = null;
let cprActive = false;
let compressionTimestamps = [];
let prevSample = null;
let lastPeakTime = 0;
let frameSkipCounter = 0;

// CPR Detection Config
const MIN_PEAK_GAP_MS = 250;
const CHEST_DROP_THRESHOLD = 8;
const CPM_WINDOW_MS = 20000;
const FRAME_SKIP = 1;
const TARGET_CPM = 110;
const FEEDBACK_COOLDOWN_MS = 3000;

// Metronome state
let audioCtx = null;
let metronomeActive = false;
let metronomeInterval = null;
let lastFeedbackTime = 0;

// Model loading state
let modelLoading = false;
let modelLoaded = false;

// IMMEDIATE MODEL PRELOADING
async function preloadDetector() {
    if (modelLoaded || modelLoading) return;
    
    modelLoading = true;
    console.log('[CPR Monitor] PRELOADING pose detector...');
    
    // Update loading status if function exists
    if (typeof updateLoadingStatus === 'function') {
        updateLoadingStatus('Loading AI Model', 'Downloading TensorFlow.js model (~12MB)');
    }
    
    try {
        const model = poseDetection.SupportedModels.MoveNet;
        const detectorConfig = {
            modelType: poseDetection.movenet.modelType.SINGLEPOSE_LIGHTNING,
            enableSmoothing: false,
            modelUrl: undefined
        };
        
        detector = await poseDetection.createDetector(model, detectorConfig);
        modelLoaded = true;
        modelLoading = false;
        
        console.log('[CPR Monitor] Pose detector PRELOADED and ready!');
        
        // Update loading status
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('AI Model Ready', 'Initializing pose detection');
        }
        
        // Preload audio context for metronome
        initAudio();
        
        return detector;
        
    } catch (error) {
        console.error('[CPR Monitor] Failed to preload pose detector:', error);
        modelLoading = false;
        
        // Update loading status with error
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('Model Loading Failed', 'Please refresh and try again');
        }
        
        return null;
    }
}

// Load detector
async function loadDetector() {
    if (modelLoaded && detector) {
        console.log('[CPR Monitor] Using preloaded detector');
        return detector;
    }
    
    if (modelLoading) {
        console.log('[CPR Monitor] Waiting for preload to complete...');
        while (modelLoading) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        return detector;
    }
    
    return await preloadDetector();
}

// Start CPR detection
async function startCPRDetection() {
    if (cprActive || !videoEl || !overlay) return;
    
    console.log('[CPR Monitor] Starting CPR detection...');
    
    try {
        const detectorInstance = await loadDetector();
        
        if (!detectorInstance) {
            console.warn('[CPR Monitor] No pose detector available');
            showCameraStatus('AI model unavailable. Camera-only mode.');
            return;
        }
        
        cprActive = true;
        compressionTimestamps = [];
        prevSample = null;
        lastPeakTime = 0;
        frameSkipCounter = 0;
        lastFeedbackTime = 0;
        
        // Start metronome
        startMetronome();
        
        // Give initial voice instruction about following the beep
        setTimeout(() => {
            speak("Listen for the beep sound. Follow this rhythm for your chest compressions. Push hard and fast on the center of the chest.", true);
        }, 1000);
        
        // Start detection loop
        requestAnimationFrame(detectionLoop);
        
        console.log('[CPR Monitor] CPR detection started');
        
    } catch (error) {
        console.error('[CPR Monitor] Failed to start CPR detection:', error);
    }
}

// Stop CPR detection
function stopCPRDetection() {
    if (!cprActive) return;
    
    console.log('[CPR Monitor] Stopping CPR detection...');
    cprActive = false;
    
    // Stop metronome
    stopMetronome();
    
    // Cancel any ongoing speech
    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
    }
    
    // Clear canvas
    if (ctx && overlay) {
        ctx.clearRect(0, 0, overlay.width, overlay.height);
    }
    
    // Hide coaching feedback
    const feedbackEl = document.getElementById('cpr-coaching-feedback');
    if (feedbackEl) {
        feedbackEl.style.display = 'none';
    }
    
    // Reset displays
    updateCPRDisplays(0, 0);
}

// Main detection loop
async function detectionLoop() {
    if (!cprActive || !detector || !videoEl) return;
    
    // Skip frames for better performance
    frameSkipCounter++;
    if (frameSkipCounter < FRAME_SKIP) {
        return requestAnimationFrame(detectionLoop);
    }
    frameSkipCounter = 0;
    
    try {
        const poses = await detector.estimatePoses(videoEl, { 
            maxPoses: 1,
            flipHorizontal: true 
        });
        
        // Clear canvas
        ctx.clearRect(0, 0, overlay.width, overlay.height);
        
        // Draw guidance overlay
        drawGuidanceOverlay();
        
        if (poses && poses.length > 0) {
            const person = poses[0];
            processPoseData(person);
        }
        
    } catch (error) {
        console.error('[CPR Monitor] Detection error:', error);
    }
    
    requestAnimationFrame(detectionLoop);
}

// Process pose data for CPR detection
function processPoseData(person) {
    const kp = {};
    person.keypoints.forEach(k => kp[k.name] = k);
    
    const leftWrist = kp.left_wrist;
    const rightWrist = kp.right_wrist;
    
    if (leftWrist && rightWrist && leftWrist.score > 0.3 && rightWrist.score > 0.3) {
        const wristY = (leftWrist.y + rightWrist.y) / 2;
        const now = Date.now();
        
        // Draw wrist positions
        drawWristPositions(leftWrist, rightWrist);
        
        // Detect compressions
        if (!prevSample) prevSample = { y: wristY, t: now };
        
        const dy = wristY - prevSample.y;
        
        if (dy > CHEST_DROP_THRESHOLD && (now - lastPeakTime) > MIN_PEAK_GAP_MS) {
            compressionTimestamps.push(now);
            lastPeakTime = now;
            
            // Visual feedback for compression
            drawCompressionFeedback();
        }
        
        prevSample = { y: wristY, t: now };
        
        // Update displays
        const cpm = computeCPM();
        updateCPRDisplays(cpm, compressionTimestamps.length);
    }
}

// Draw guidance overlay
function drawGuidanceOverlay() {
    const centerX = overlay.width / 2;
    const centerY = overlay.height / 2;
    
    ctx.save();
    
    // Semi-transparent background
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, overlay.width, overlay.height);
    
    // Chest compression target area
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.setLineDash([10, 5]);
    ctx.beginPath();
    ctx.rect(centerX - 80, centerY - 40, 160, 80);
    ctx.stroke();
    
    // Hand position guides
    ctx.setLineDash([]);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    
    // Left hand guide
    ctx.beginPath();
    ctx.moveTo(centerX - 100, centerY - 60);
    ctx.lineTo(centerX - 60, centerY - 20);
    ctx.lineTo(centerX - 40, centerY);
    ctx.stroke();
    
    // Right hand guide
    ctx.beginPath();
    ctx.moveTo(centerX + 100, centerY - 60);
    ctx.lineTo(centerX + 60, centerY - 20);
    ctx.lineTo(centerX + 40, centerY);
    ctx.stroke();
    
    ctx.restore();
}

// Draw wrist positions
function drawWristPositions(leftWrist, rightWrist) {
    ctx.fillStyle = '#ff4444';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    
    // Left wrist
    ctx.beginPath();
    ctx.arc(leftWrist.x, leftWrist.y, 10, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Right wrist
    ctx.beginPath();
    ctx.arc(rightWrist.x, rightWrist.y, 10, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Connection line
    ctx.strokeStyle = '#ff4444';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(leftWrist.x, leftWrist.y);
    ctx.lineTo(rightWrist.x, rightWrist.y);
    ctx.stroke();
}

// Draw compression feedback
function drawCompressionFeedback() {
    ctx.fillStyle = 'rgba(0, 255, 0, 0.4)';
    ctx.fillRect(0, 0, overlay.width, overlay.height);
    
    ctx.fillStyle = '#00ff00';
    ctx.font = 'bold 24px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('COMPRESSION!', overlay.width / 2, 50);
}

// Compute CPM (Compressions Per Minute)
function computeCPM() {
    const now = Date.now();
    compressionTimestamps = compressionTimestamps.filter(t => now - t <= CPM_WINDOW_MS);
    
    if (compressionTimestamps.length < 2) return 0;
    
    const intervals = [];
    for (let i = 1; i < compressionTimestamps.length; i++) {
        intervals.push(compressionTimestamps[i] - compressionTimestamps[i - 1]);
    }
    
    const avg = intervals.reduce((a, b) => a + b, 0) / intervals.length;
    return Math.round(60000 / avg);
}

// Update CPR displays
function updateCPRDisplays(cpm, count) {
    const cpmDisplay = document.getElementById('cpm-display');
    const compressionCount = document.getElementById('compression-count');
    const miniOverlay = document.getElementById('cpr-mini-overlay');
    
    if (cpmDisplay) {
        cpmDisplay.textContent = cpm || '—';
        
        // Color coding
        if (cpm >= 100 && cpm <= 120) {
            cpmDisplay.style.color = '#28a745'; // Green - good
        } else if (cpm > 0) {
            cpmDisplay.style.color = '#ffc107'; // Yellow - needs adjustment
        } else {
            cpmDisplay.style.color = '#666'; // Gray - no data
        }
    }
    
    if (compressionCount) {
        compressionCount.textContent = count;
    }
    
    if (miniOverlay) {
        miniOverlay.textContent = `Rate: ${cpm || '—'} CPM`;
    }
    
    // Provide coaching feedback
    if (count >= 5) {
        provideCPRCoaching(cpm);
    }
}

// =============== METRONOME SYSTEM ===============
function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playBeep() {
    if (!audioCtx) initAudio();
    
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
    
    oscillator.start(audioCtx.currentTime);
    oscillator.stop(audioCtx.currentTime + 0.1);
}

function startMetronome() {
    if (metronomeActive) return;
    
    initAudio();
    metronomeActive = true;
    
    const interval = 60000 / TARGET_CPM;
    
    playBeep();
    
    metronomeInterval = setInterval(() => {
        if (metronomeActive) {
            playBeep();
        }
    }, interval);
    
    console.log('[CPR Monitor] Metronome started at', TARGET_CPM, 'BPM');
}

function stopMetronome() {
    metronomeActive = false;
    
    if (metronomeInterval) {
        clearInterval(metronomeInterval);
        metronomeInterval = null;
    }
    
    if (audioCtx) {
        try {
            audioCtx.close();
            audioCtx = null;
        } catch (e) {
            console.error('[CPR Monitor] Error closing audio context:', e);
        }
    }
    
    console.log('[CPR Monitor] Metronome stopped');
}

// =============== VOICE COACHING SYSTEM ===============
function speak(text, priority = false) {
    if (!text || !window.speechSynthesis) return;
    
    try {
        // Cancel previous speech if priority message
        if (priority) {
            window.speechSynthesis.cancel();
        }
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0; // Clear, normal speed
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        utterance.lang = 'en-US';
        
        window.speechSynthesis.speak(utterance);
        console.log('[CPR Coach] Speaking:', text);
        
    } catch (error) {
        console.error('[CPR Coach] Speech error:', error);
    }
}

function provideCPRCoaching(cpm) {
    const now = Date.now();
    
    // Provide coaching feedback every 3 seconds
    if (now - lastFeedbackTime < FEEDBACK_COOLDOWN_MS) return;
    
    lastFeedbackTime = now;
    
    let voiceMessage = '';
    let displayMessage = '';
    
    if (cpm === 0) {
        voiceMessage = "Begin chest compressions now. Follow the beep rhythm.";
        displayMessage = "Start Compressions";
    } else if (cpm < 90) {
        voiceMessage = `Too slow. Increase your speed. Current rate ${cpm} per minute.`;
        displayMessage = `Too Slow: ${cpm} CPM`;
    } else if (cpm >= 90 && cpm < 100) {
        voiceMessage = `Speed up slightly. You're at ${cpm} compressions per minute.`;
        displayMessage = `Speed Up: ${cpm} CPM`;
    } else if (cpm >= 100 && cpm <= 120) {
        voiceMessage = `Perfect rhythm! Keep going at ${cpm} compressions per minute.`;
        displayMessage = `Perfect: ${cpm} CPM`;
    } else if (cpm > 120 && cpm <= 140) {
        voiceMessage = `Slow down a bit. You're going ${cpm} per minute.`;
        displayMessage = `Slow Down: ${cpm} CPM`;
    } else {
        voiceMessage = `Too fast. Reduce your pace. Follow the beep rhythm.`;
        displayMessage = `Too Fast: ${cpm} CPM`;
    }
    
    // Speak the coaching message
    speak(voiceMessage, true);
    
    // Show visual feedback
    showRateFeedback(displayMessage, cpm);
}

function showRateFeedback(message, cpm) {
    let feedbackEl = document.getElementById('cpr-coaching-feedback');
    
    if (!feedbackEl) {
        feedbackEl = document.createElement('div');
        feedbackEl.id = 'cpr-coaching-feedback';
        feedbackEl.style.cssText = `
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            z-index: 300;
            text-align: center;
            min-width: 200px;
            transition: all 0.3s ease;
        `;
        
        if (overlay && overlay.parentElement) {
            overlay.parentElement.appendChild(feedbackEl);
        }
    }
    
    // Color code based on CPM
    let backgroundColor = 'rgba(0, 0, 0, 0.8)';
    if (cpm >= 100 && cpm <= 120) {
        backgroundColor = 'rgba(40, 167, 69, 0.9)'; // Green
    } else if (cpm > 0) {
        backgroundColor = 'rgba(255, 193, 7, 0.9)'; // Yellow
    } else {
        backgroundColor = 'rgba(220, 53, 69, 0.9)'; // Red
    }
    
    feedbackEl.style.background = backgroundColor;
    feedbackEl.textContent = message;
    feedbackEl.style.display = 'block';
    feedbackEl.style.opacity = '1';
    
    // Auto-hide after 4 seconds
    setTimeout(() => {
        if (feedbackEl) {
            feedbackEl.style.opacity = '0';
            setTimeout(() => {
                if (feedbackEl) {
                    feedbackEl.style.display = 'none';
                }
            }, 300);
        }
    }, 4000);
}

// =============== CAMERA SYSTEM ===============
async function startCamera() {
    if (cameraActive || !videoEl) return;
    
    console.log('[CPR Monitor] Starting camera...');
    
    try {
        // Update loading status
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('Accessing Camera', 'Please allow camera permissions');
        }
        
        showCameraStatus('Camera starting...');
        
        const constraints = {
            video: { 
                facingMode: "user",
                width: { ideal: 320, max: 480 },
                height: { ideal: 240, max: 360 },
                frameRate: { ideal: 20, max: 30 }
            },
            audio: false
        };
        
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        videoEl.srcObject = stream;
        
        // Update loading status
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('Camera Connected', 'Initializing video stream');
        }
        
        await new Promise((resolve) => {
            videoEl.onloadedmetadata = () => {
                videoEl.play().then(resolve);
            };
        });
        
        if (overlay) {
            overlay.width = videoEl.videoWidth || 320;
            overlay.height = videoEl.videoHeight || 240;
            ctx = overlay.getContext('2d');
        }
        
        cameraActive = true;
        hideCameraStatus();
        
        // Update loading status
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('Starting Detection', 'Initializing pose detection');
        }
        
        startCPRDetection();
        
        console.log('[CPR Monitor] Camera started and CPR detection active!');
        
        // Hide loading overlay after everything is ready
        setTimeout(() => {
            if (typeof hideLoadingOverlay === 'function') {
                hideLoadingOverlay();
            }
        }, 1000);
        
    } catch (error) {
        console.error('[CPR Monitor] Camera error:', error);
        showCameraStatus('Camera access denied. Please allow camera permissions and refresh.');
        
        // Update loading status with error
        if (typeof updateLoadingStatus === 'function') {
            updateLoadingStatus('Camera Access Denied', 'Please allow camera permissions and refresh');
        }
    }
}

function stopCamera() {
    if (!cameraActive) return;
    
    console.log('[CPR Monitor] Stopping camera...');
    
    stopCPRDetection();
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    if (videoEl) {
        videoEl.srcObject = null;
    }
    
    cameraActive = false;
    console.log('[CPR Monitor] Camera stopped');
}

function showCameraStatus(message) {
    const statusEl = document.getElementById('cpr-camera-status');
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.style.display = 'block';
    }
}

function hideCameraStatus() {
    const statusEl = document.getElementById('cpr-camera-status');
    if (statusEl) {
        statusEl.style.display = 'none';
    }
}

// Initialize
function initCPRMonitor() {
    console.log('[CPR Monitor] Initializing...');
    
    bottomSheet = document.getElementById('cpr-bottom-sheet');
    dragHandle = document.getElementById('drag-handle');
    videoEl = document.getElementById('cpr-video');
    overlay = document.getElementById('cpr-overlay');
    
    if (!bottomSheet) {
        console.error('[CPR Monitor] Bottom sheet element not found!');
        return;
    }
    
    // Close button
    const closeBtn = document.getElementById('cpr-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            stopCamera();
        });
    }
    
    console.log('[CPR Monitor] Initialized successfully');
}

// Show monitor
function showCPRMonitor() {
    console.log('[CPR Monitor] Starting CPR monitor...');
    
    if (!bottomSheet) {
        console.error('[CPR Monitor] Monitor not initialized');
        return;
    }
    
    bottomSheet.style.display = 'block';
    bottomSheet.style.visibility = 'visible';
    bottomSheet.style.opacity = '1';
    
    // Start camera immediately
    if (videoEl && !cameraActive) {
        startCamera();
    }
    
    console.log('[CPR Monitor] CPR monitor started');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCPRMonitor);
} else {
    initCPRMonitor();
}

// Export to global scope
window.CPRMonitor = {
    show: showCPRMonitor,
    start: startCamera,
    stop: stopCamera,
    debug: () => {
        console.log('[CPR Monitor] Debug info:');
        console.log('- Model loaded:', modelLoaded);
        console.log('- Camera active:', cameraActive);
        console.log('- CPR active:', cprActive);
        console.log('- Compressions:', compressionTimestamps.length);
    }
};

console.log('[CPR Monitor] Minimal pose detection model loaded and ready');