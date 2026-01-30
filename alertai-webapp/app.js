// AlertAI Web App JavaScript
class AlertAI {
    constructor() {
        this.user = null;
        this.location = null;
        this.alerts = [];
        this.alertHistory = [];
        
        // Use configuration from config.js or URL parameter
        const urlParams = new URLSearchParams(window.location.search);
        const serverUrl = urlParams.get('server') || 
                         (window.AlertAIConfig && window.AlertAIConfig.serverUrl) || 
                         'http://localhost:5000';
        this.serverUrl = serverUrl;
        
        console.log('AlertAI: Using server URL:', this.serverUrl);
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkExistingUser();
        this.updateConnectionStatus();
        
        // Check for location updates every 30 seconds
        setInterval(() => {
            if (this.user && this.location) {
                this.updateLocation();
            }
        }, 30000);

        // Simulate receiving emergency alerts (in real app, this would be push notifications)
        this.simulateEmergencyAlerts();
    }

    setupEventListeners() {
        // Registration form
        document.getElementById('registrationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.registerUser();
        });

        // Location enable button
        document.getElementById('enableLocation').addEventListener('click', () => {
            this.enableLocation();
        });

        // Form validation
        const inputs = document.querySelectorAll('#registrationForm input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateForm();
            });
        });
    }

    checkExistingUser() {
        const savedUser = localStorage.getItem('alertai_user');
        if (savedUser) {
            this.user = JSON.parse(savedUser);
            this.showDashboard();
            this.updateLocation();
        }
    }

    async enableLocation() {
        const button = document.getElementById('enableLocation');
        const status = document.getElementById('locationStatus');
        
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting Location...';
        
        try {
            const position = await this.getCurrentPosition();
            this.location = {
                lat: position.coords.latitude,
                lon: position.coords.longitude,
                accuracy: position.coords.accuracy,
                timestamp: new Date().toISOString()
            };

            status.className = 'location-status success';
            status.innerHTML = `
                <i class="fas fa-check-circle"></i> 
                Location enabled! Accuracy: ${Math.round(this.location.accuracy)}m
            `;
            
            button.innerHTML = '<i class="fas fa-check"></i> Location Enabled';
            this.validateForm();
            
        } catch (error) {
            status.className = 'location-status error';
            status.innerHTML = `
                <i class="fas fa-exclamation-circle"></i> 
                Location access denied. Please enable location permissions.
            `;
            button.innerHTML = '<i class="fas fa-crosshairs"></i> Enable Location Access';
            button.disabled = false;
        }
    }

    getCurrentPosition() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation not supported'));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                resolve,
                reject,
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 60000
                }
            );
        });
    }

    validateForm() {
        const name = document.getElementById('userName').value.trim();
        const phone = document.getElementById('userPhone').value.trim();
        const email = document.getElementById('userEmail').value.trim();
        const hasLocation = this.location !== null;
        
        const isValid = name && phone && email && hasLocation;
        document.getElementById('registerBtn').disabled = !isValid;
    }

    async registerUser() {
        const userData = {
            name: document.getElementById('userName').value.trim(),
            phone: document.getElementById('userPhone').value.trim(),
            email: document.getElementById('userEmail').value.trim(),
            location: this.location
        };

        try {
            // Send registration to Flask server
            const response = await fetch(`${this.serverUrl}/api/users/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                const result = await response.json();
                
                // Save user data with server-assigned ID
                this.user = {
                    ...userData,
                    user_id: result.user_id,
                    registeredAt: new Date().toISOString()
                };
                
                localStorage.setItem('alertai_user', JSON.stringify(this.user));

                console.log('User registered with server:', result);
                this.showDashboard();
                this.showNotification('Registration successful! You will now receive emergency alerts.', 'success');
                
                // Start location updates
                this.startLocationUpdates();
            } else {
                const error = await response.json();
                throw new Error(error.error || 'Registration failed');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showNotification(`Registration failed: ${error.message}`, 'error');
        }
    }

    showDashboard() {
        document.getElementById('registrationPanel').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';

        // Update user display
        document.getElementById('displayName').textContent = this.user.name;
        document.getElementById('displayPhone').textContent = this.user.phone;
        this.updateLocationDisplay();
    }

    async updateLocation() {
        try {
            const position = await this.getCurrentPosition();
            this.location = {
                lat: position.coords.latitude,
                lon: position.coords.longitude,
                accuracy: position.coords.accuracy,
                timestamp: new Date().toISOString()
            };
            
            this.updateLocationDisplay();
            
            // Send location update to server if user is registered
            if (this.user && this.user.user_id) {
                try {
                    await fetch(`${this.serverUrl}/api/users/location`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            user_id: this.user.user_id,
                            location: this.location
                        })
                    });
                    console.log('Location updated on server');
                } catch (error) {
                    console.error('Failed to update location on server:', error);
                }
            }
            
        } catch (error) {
            console.error('Failed to update location:', error);
        }
    }

    startLocationUpdates() {
        // Update location every 30 seconds
        this.locationInterval = setInterval(() => {
            this.updateLocation();
        }, 30000);
    }

    updateLocationDisplay() {
        if (this.location) {
            const lat = this.location.lat.toFixed(6);
            const lon = this.location.lon.toFixed(6);
            document.getElementById('displayLocation').textContent = `${lat}, ${lon}`;
        }
    }

    updateConnectionStatus() {
        // Check actual server connection
        fetch(`${this.serverUrl}/health`)
            .then(response => {
                const statusDot = document.getElementById('connectionStatus');
                const statusText = document.getElementById('statusText');
                
                if (response.ok) {
                    statusDot.className = 'status-dot connected';
                    statusText.textContent = 'Connected to AlertAI Server';
                } else {
                    statusDot.className = 'status-dot disconnected';
                    statusText.textContent = 'Server Connection Issues';
                }
            })
            .catch(error => {
                const statusDot = document.getElementById('connectionStatus');
                const statusText = document.getElementById('statusText');
                
                statusDot.className = 'status-dot disconnected';
                statusText.textContent = 'Server Offline';
                console.error('Server connection failed:', error);
            });
    }

    // Emergency Alert System
    async loadActiveAlerts() {
        try {
            const response = await fetch(`${this.serverUrl}/api/alerts/active`);
            if (response.ok) {
                const data = await response.json();
                
                // Clear existing alerts first
                this.alerts = [];
                
                // Process active alerts from server
                data.alerts.forEach(alert => {
                    this.processServerAlert(alert);
                });
                
                // Update display
                this.updateAlertsDisplay();
            }
        } catch (error) {
            console.error('Failed to load active alerts:', error);
        }
    }

    processServerAlert(alertData) {
        // Check if we already have this alert to prevent duplicates
        const existingAlert = this.alerts.find(alert => alert.id === alertData.id);
        if (existingAlert) {
            return; // Skip duplicate alert
        }

        // Check if this alert was already seen (stored in localStorage)
        const seenAlerts = JSON.parse(localStorage.getItem('alertai_seen_alerts') || '[]');
        const alreadySeen = seenAlerts.includes(alertData.id);

        // Convert server emergency format to web app alert format
        const webAlert = {
            id: alertData.id,
            emergency_type: alertData.emergency_type,
            location: alertData.location,
            building: alertData.building,
            timestamp: alertData.timestamp,
            distance_meters: this.calculateDistance(alertData.location),
            message: this.createAlertMessage(alertData),
            alreadySeen: alreadySeen
        };

        // Add to alerts list
        this.alerts.push(webAlert);
        
        // Add to history if not already there
        const existingInHistory = this.alertHistory.find(alert => alert.id === alertData.id);
        if (!existingInHistory) {
            this.alertHistory.unshift(webAlert);
        }

        // Only show modal for NEW alerts (not previously seen)
        if (!alreadySeen) {
            this.showEmergencyAlert(webAlert);
            this.playAlertSound();
            
            // Mark as seen
            seenAlerts.push(alertData.id);
            localStorage.setItem('alertai_seen_alerts', JSON.stringify(seenAlerts));
        }

        // Always update display
        this.updateAlertsDisplay();
    }

    calculateDistance(emergencyLocation) {
        if (!this.location) return 0;
        
        // Simple distance calculation (you can use the haversine formula)
        const lat1 = this.location.lat;
        const lon1 = this.location.lon;
        const lat2 = emergencyLocation.lat;
        const lon2 = emergencyLocation.lon;
        
        const R = 6371000; // Earth's radius in meters
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return Math.round(R * c);
    }

    createAlertMessage(alertData) {
        const distance = this.calculateDistance(alertData.location);
        return `🚨 ${alertData.emergency_type.toUpperCase()} EMERGENCY: ${alertData.emergency_type} detected at ${alertData.building}. You are ${distance}m away. Please follow safety protocols.`;
    }

    getEmergencyInstructions(emergencyType) {
        const instructions = {
            'Fire': 'Exit the building immediately using the nearest fire exit. Do not use elevators. Proceed to the designated assembly point.',
            'Accident': 'Stay clear of the accident area. If trained in first aid and safe to do so, provide assistance. Call emergency services.',
            'Smoke': 'Exit the area immediately. Stay low to avoid smoke inhalation. Use stairs, not elevators. Report to assembly point.',
            'Fallen Person': 'If you are trained in first aid, consider assisting. Otherwise, ensure emergency services have been contacted. Do not move the person unless in immediate danger.',
            'Gun': 'IMMEDIATE DANGER: Run, Hide, Fight. Evacuate if safe to do so. Hide if evacuation is not possible. Call emergency services immediately.',
            'Blood': 'If you are trained in first aid and it is safe, provide assistance. Apply pressure to bleeding wounds. Call emergency services immediately.'
        };
        
        return instructions[emergencyType] || 'Follow emergency protocols and contact emergency services if needed.';
    }

    simulateEmergencyAlerts() {
        // Load real alerts from server
        this.loadActiveAlerts();
        
        // Check for new alerts every 30 seconds
        setInterval(() => {
            this.loadActiveAlerts();
        }, 30000);

        // No demo alerts - only show real emergencies from server
        console.log('AlertAI: Monitoring for real emergency alerts from server...');
    }

    receiveEmergencyAlert(alertData) {
        // This method is now only used for manual alert injection
        // Real server alerts are handled by processServerAlert()
        if (!this.user) return;

        // Check if we already have this alert
        const existingAlert = this.alerts.find(alert => alert.id === alertData.id);
        if (existingAlert) {
            return; // Skip duplicate
        }

        // Add to active alerts
        this.alerts.push(alertData);
        
        // Add to history if not already there
        const existingInHistory = this.alertHistory.find(alert => alert.id === alertData.id);
        if (!existingInHistory) {
            this.alertHistory.unshift(alertData);
        }

        // Show alert modal for manual alerts
        this.showEmergencyAlert(alertData);

        // Update alerts display
        this.updateAlertsDisplay();

        // Play alert sound (in a real app)
        this.playAlertSound();
    }

    showEmergencyAlert(alert) {
        const modal = document.getElementById('alertModal');
        const icon = document.getElementById('alertIcon');
        const title = document.getElementById('alertTitle');
        const type = document.getElementById('alertType');
        const location = document.getElementById('alertLocation');
        const distance = document.getElementById('alertDistance');
        const time = document.getElementById('alertTime');
        const message = document.getElementById('alertMessage');
        const guidanceBtn = document.getElementById('guidanceAgentBtn');

        // Set alert icon based on type
        const icons = {
            'Fire': 'fas fa-fire',
            'Accident': 'fas fa-car-crash',
            'Smoke': 'fas fa-smog',
            'Fallen Person': 'fas fa-user-injured',
            'Gun': 'fas fa-exclamation-circle',
            'Blood': 'fas fa-tint'
        };

        icon.innerHTML = `<i class="${icons[alert.emergency_type] || 'fas fa-exclamation-triangle'}"></i>`;
        title.textContent = `${alert.emergency_type.toUpperCase()} EMERGENCY`;
        type.textContent = `Emergency Type: ${alert.emergency_type}`;
        location.textContent = `Location: ${alert.building}`;
        distance.textContent = `Distance: ${alert.distance_meters}m away`;
        time.textContent = `Time: ${new Date(alert.timestamp).toLocaleString()}`;
        message.textContent = alert.message;

        // Update guidance agent button text based on emergency type
        if (guidanceBtn) {
            const agentTypes = {
                'Fire': 'Fire Safety Agent',
                'Smoke': 'Smoke Safety Agent',
                'Fallen Person': 'Medical Response Agent',
                'Gun': 'Security Response Agent',
                'Blood': 'Trauma Response Agent'
            };
            
            const agentName = agentTypes[alert.emergency_type] || 'Guidance Agent';
            guidanceBtn.innerHTML = `<i class="fas fa-robot"></i> Start ${agentName}`;
            guidanceBtn.disabled = false;
            guidanceBtn.style.background = '#3498db';
        }

        modal.classList.add('show');
        
        // Store current alert for actions
        this.currentAlert = alert;
    }

    updateAlertsDisplay() {
        const alertsList = document.getElementById('alertsList');
        const historyList = document.getElementById('historyList');

        // Update active alerts
        if (this.alerts.length === 0) {
            alertsList.innerHTML = `
                <div class="no-alerts">
                    <i class="fas fa-check-circle"></i>
                    <p>No active emergencies in your area</p>
                </div>
            `;
        } else {
            alertsList.innerHTML = this.alerts.map(alert => `
                <div class="alert-item active">
                    <h4><i class="fas fa-exclamation-triangle"></i> ${alert.emergency_type}</h4>
                    <p><strong>Location:</strong> ${alert.building}</p>
                    <p><strong>Distance:</strong> ${alert.distance_meters}m</p>
                    <p><strong>Time:</strong> ${new Date(alert.timestamp).toLocaleString()}</p>
                </div>
            `).join('');
        }

        // Update history
        if (this.alertHistory.length === 0) {
            historyList.innerHTML = '<p class="no-history">No previous alerts</p>';
        } else {
            historyList.innerHTML = this.alertHistory.slice(0, 10).map(alert => `
                <div class="alert-item resolved">
                    <h4><i class="fas fa-check"></i> ${alert.emergency_type}</h4>
                    <p><strong>Location:</strong> ${alert.building}</p>
                    <p><strong>Distance:</strong> ${alert.distance_meters}m</p>
                    <p><strong>Time:</strong> ${new Date(alert.timestamp).toLocaleString()}</p>
                </div>
            `).join('');
        }
    }

    playAlertSound() {
        // In a real app, play emergency alert sound
        console.log('🔊 Playing emergency alert sound');
    }

    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#27ae60' : '#3498db'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 1001;
            animation: slideIn 0.3s;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    clearSeenAlerts() {
        // Clear the seen alerts cache (for testing)
        localStorage.removeItem('alertai_seen_alerts');
        console.log('Cleared seen alerts cache');
    }
}

// Global functions for modal actions
// Emergency services are automatically notified - no manual call needed

function startGuidanceAgent() {
    if (!window.alertAI || !window.alertAI.currentAlert) {
        alert('No active alert found');
        return;
    }

    const alert = window.alertAI.currentAlert;
    const emergencyType = alert.emergency_type;
    
    // Map emergency types to agent commands
    const agentCommands = {
        'Fire': 'python alertai-agent/fire_emergency_agent.py',
        'Smoke': 'python alertai-agent/smoke_emergency_agent.py', 
        'Fallen Person': 'python alertai-agent/fallen_person_agent.py',
        'Gun': 'python alertai-agent/gun_emergency_agent.py',
        'Blood': 'python alertai-agent/blood_emergency_agent.py'
    };

    const command = agentCommands[emergencyType];
    
    if (!command) {
        alert(`No guidance agent available for ${emergencyType} emergencies yet.`);
        return;
    }

    // Update button to show launching state
    const button = document.getElementById('guidanceAgentBtn');
    if (button) {
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Launching Agent...';
        button.disabled = true;
        button.style.background = '#f39c12';
    }

    // Launch the guidance interface
    const guidanceUrl = `guidance.html?type=${encodeURIComponent(emergencyType)}&building=${encodeURIComponent(alert.building)}&floor=${encodeURIComponent(alert.floor_affected || 'Unknown')}`;
    
    // Open in new window/tab for better experience
    const guidanceWindow = window.open(guidanceUrl, 'AlertAI_Guidance', 'width=1200,height=800,scrollbars=no,resizable=yes');
    
    if (guidanceWindow) {
        // Focus the new window
        guidanceWindow.focus();
        
        // Update button to show launched state
        if (button) {
            button.innerHTML = '<i class="fas fa-external-link-alt"></i> Agent Active';
            button.style.background = '#27ae60';
        }
        
        // Show success notification
        showLaunchNotification(emergencyType, 'success');
        console.log(`🤖 Guidance Agent launched for ${emergencyType} emergency`);
        
        // Automatically attempt to launch terminal agent for debugging (silent)
        launchTerminalAgent(emergencyType, alert);
        
    } else {
        // Popup was blocked - show fallback
        if (button) {
            button.innerHTML = '<i class="fas fa-robot"></i> Start Agent';
            button.disabled = false;
            button.style.background = '#e74c3c';
        }
        
        showLaunchNotification(emergencyType, 'blocked', {
            guidanceUrl: `${window.location.origin}/${guidanceUrl}`,
            command: command
        });
    }
}

// Improved launch notification system
function showLaunchNotification(emergencyType, status, fallbackData = null) {
    const notification = document.createElement('div');
    notification.className = 'launch-notification';
    
    let content = '';
    let bgColor = '#27ae60';
    let icon = 'fas fa-check-circle';
    
    switch (status) {
        case 'success':
            content = `
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <i class="${icon}" style="margin-right: 8px; color: white;"></i>
                    <strong>${emergencyType} Agent Launched</strong>
                </div>
                <div style="font-size: 14px; opacity: 0.9;">
                    ✅ Web guidance interface opened<br>
                    🖥️ Terminal agent starting (for debugging)
                </div>
                <div style="margin-top: 10px; font-size: 12px; opacity: 0.7;">
                    Follow the step-by-step guidance in the new window
                </div>
            `;
            break;
            
        case 'blocked':
            bgColor = '#e74c3c';
            icon = 'fas fa-exclamation-triangle';
            content = `
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <i class="${icon}" style="margin-right: 8px; color: white;"></i>
                    <strong>Popup Blocked</strong>
                </div>
                <div style="font-size: 14px; opacity: 0.9;">
                    Please allow popups for this site, then try again
                </div>
                <div style="margin-top: 10px;">
                    <button onclick="window.open('${fallbackData.guidanceUrl}', '_blank')" 
                            style="background: white; color: #e74c3c; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 12px;">
                        Open Guidance Manually
                    </button>
                </div>
            `;
            break;
            
        case 'terminal-success':
            bgColor = '#3498db';
            icon = 'fas fa-terminal';
            content = `
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <i class="${icon}" style="margin-right: 8px; color: white;"></i>
                    <strong>Terminal Agent Active</strong>
                </div>
                <div style="font-size: 14px; opacity: 0.9;">
                    ${emergencyType} debugging console opened<br>
                    Check your terminal for conversation details
                </div>
            `;
            break;
    }
    
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${bgColor};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1002;
            max-width: 350px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            animation: slideIn 0.3s ease-out;
        ">
            ${content}
        </div>
    `;
    
    // Add slide-in animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Auto-remove notification
    const duration = status === 'blocked' ? 15000 : 8000; // Longer for error messages
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, duration);
}

// Simplified terminal agent launcher (silent, no user prompts)
function launchTerminalAgent(emergencyType, alertData) {
    // Send request to server to launch terminal agent
    fetch('/api/launch-agent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            emergency_type: emergencyType,
            alert_data: alertData,
            launch_terminal: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('🖥️ Terminal agent launched successfully');
            // Show subtle notification that terminal is running
            setTimeout(() => {
                showLaunchNotification(emergencyType, 'terminal-success');
            }, 2000); // Delay to avoid notification overlap
        } else {
            console.log('⚠️ Terminal agent launch failed:', data.error);
        }
    })
    .catch(error => {
        console.log('⚠️ Could not auto-launch terminal agent:', error);
    });
}



function acknowledgeAlert() {
    const modal = document.getElementById('alertModal');
    modal.classList.remove('show');
    
    // Reset guidance agent button
    const button = document.getElementById('guidanceAgentBtn');
    if (button) {
        button.innerHTML = '<i class="fas fa-robot"></i> Start Guidance Agent';
        button.disabled = false;
        button.style.background = '#3498db';
    }
    
    // Remove from active alerts
    if (window.alertAI && window.alertAI.currentAlert) {
        const alertId = window.alertAI.currentAlert.id;
        window.alertAI.alerts = window.alertAI.alerts.filter(alert => alert.id !== alertId);
        window.alertAI.updateAlertsDisplay();
    }
}

// Emergency Simulation Function
async function simulateEmergency(emergencyType) {
    console.log(`Simulating ${emergencyType} emergency...`);
    
    // Show loading state on the button
    const buttons = document.querySelectorAll('.sim-btn');
    buttons.forEach(btn => {
        if (btn.textContent.includes(emergencyType)) {
            btn.style.opacity = '0.7';
            btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i><span>Sending...</span>`;
            btn.disabled = true;
        }
    });
    
    try {
        // Define specific locations for each emergency type
        const emergencyLocations = {
            'Fire': {
                floor: '1st Floor',
                specific_location: 'Corridor near elevator',
                room_details: 'Patient care area, Room 105',
                affected_areas: ['Corridor near elevator', 'Adjacent patient rooms', 'Nursing station'],
                equipment_nearby: ['ABC Dry Chemical extinguisher (10 lbs)', 'Emergency stairwell access'],
                hazards: ['Medical oxygen supply system', 'Electrical equipment']
            },
            'Smoke': {
                floor: 'Ground Floor',
                specific_location: 'Kitchen area',
                room_details: 'Main kitchen facility',
                affected_areas: ['Kitchen area', 'Dining hall', 'Food storage'],
                equipment_nearby: ['Class K Wet Chemical extinguisher (6 lbs)', 'Fire suppression system'],
                hazards: ['Natural gas lines', 'Cooking equipment', 'Ventilation system']
            },
            'Accident': {
                floor: 'Ground Floor',
                specific_location: 'Main entrance lobby',
                room_details: 'Reception and waiting area',
                affected_areas: ['Main entrance', 'Reception desk', 'Waiting area'],
                equipment_nearby: ['First aid station', 'Emergency communication system'],
                hazards: ['High foot traffic area', 'Glass surfaces']
            },
            'Fallen Person': {
                floor: '2nd Floor',
                specific_location: 'Conference room',
                room_details: 'Conference Room B, near administrative offices',
                affected_areas: ['Conference room', 'Administrative corridor'],
                equipment_nearby: ['Emergency communication system', 'First aid kit'],
                hazards: ['Stairs nearby', 'Office furniture']
            },
            'Gun': {
                floor: '1st Floor',
                specific_location: 'Office area',
                room_details: 'Administrative office section',
                affected_areas: ['Office area', 'Administrative corridor', 'Staff areas'],
                equipment_nearby: ['Emergency lockdown system', 'Communication devices'],
                hazards: ['Multiple exit routes needed', 'Staff and visitor safety']
            },
            'Blood': {
                floor: '1st Floor',
                specific_location: 'Patient room 108',
                room_details: 'Patient care room, medical emergency',
                affected_areas: ['Patient room 108', 'Nursing station', 'Medical supply area'],
                equipment_nearby: ['Medical supplies', 'Emergency medical equipment'],
                hazards: ['Medical oxygen supply system', 'Patient safety priority']
            }
        };
        
        const locationInfo = emergencyLocations[emergencyType];
        
        // Create comprehensive emergency data matching backend structure exactly
        const emergencyData = {
            id: Date.now(), // Unique ID based on timestamp
            emergency_type: emergencyType,
            location: {
                lat: 11.849010,
                lon: 13.056751
            },
            building: "Medical Center Building A",
            floor_affected: locationInfo.floor,
            specific_location: locationInfo.specific_location,
            room_details: locationInfo.room_details,
            affected_areas: locationInfo.affected_areas,
            equipment_nearby: locationInfo.equipment_nearby,
            potential_hazards: locationInfo.hazards,
            timestamp: new Date().toISOString(),
            image_url: `test_images/${emergencyType.toLowerCase().replace(' ', '_')}_emergency.jpg`,
            created_at: new Date().toISOString(),
            
            // Complete building layout information (matches backend API structure)
            building_layout: {
                floors: ["Ground Floor", "1st Floor", "2nd Floor"],
                fire_extinguishers: {
                    "Ground Floor": [
                        {"location": "Near main entrance", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Kitchen area", "type": "Class K (Wet Chemical)", "capacity": "6 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Electrical room", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
                    ],
                    "1st Floor": [
                        {"location": "Corridor near elevator", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Emergency stairwell", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
                        {"location": "Office area", "type": "CO2", "capacity": "10 lbs", "last_inspection": "2024-01-10"}
                    ],
                    "2nd Floor": [
                        {"location": "Near conference room", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Break room", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
                        {"location": "Emergency exit", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
                    ]
                },
                emergency_exits: {
                    "Ground Floor": [
                        {"name": "Main entrance", "direction": "Front of building", "capacity": "200 people", "width": "Double doors"},
                        {"name": "Back exit near parking", "direction": "Rear parking lot", "capacity": "150 people", "width": "Single door"}
                    ],
                    "1st Floor": [
                        {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"}
                    ],
                    "2nd Floor": [
                        {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Fire escape", "direction": "North side", "capacity": "50 people", "width": "External ladder"}
                    ]
                },
                special_hazards: {
                    "Ground Floor": ["High voltage electrical equipment in server room", "Natural gas lines in kitchen area", "Oxygen tanks in medical storage"],
                    "1st Floor": ["Medical oxygen supply system", "Chemical storage room with flammables", "Server room with lithium batteries"],
                    "2nd Floor": ["Backup generators with diesel fuel", "Propane tanks for heating system", "Chemical laboratory with various substances"]
                },
                assembly_points: [
                    {"name": "Parking lot area", "capacity": "300 people", "distance": "100m from building", "safety_features": ["Open space", "Away from building"]},
                    {"name": "Front courtyard", "capacity": "200 people", "distance": "50m from building", "safety_features": ["Open space", "Near road access"]}
                ]
            },
            
            // Building information (matches backend structure)
            building_info: {
                total_floors: 3,
                max_occupancy: 500,
                construction_type: "Steel frame with concrete",
                sprinkler_system: true,
                fire_alarm_system: true,
                emergency_lighting: true
            },
            
            // Emergency contacts (matches backend structure)
            emergency_contacts: {
                fire_department: "911 or +234-911-FIRE",
                building_security: "+234-800-SECURITY",
                facility_manager: "+234-800-FACILITY",
                medical_emergency: "911 or +234-911-MEDICAL"
            },
            
            // Floor-specific information for current emergency
            current_floor_info: {
                floor: locationInfo.floor,
                fire_extinguishers: getFloorExtinguishers(locationInfo.floor),
                emergency_exits: getFloorExits(locationInfo.floor),
                special_hazards: getFloorHazards(locationInfo.floor)
            },
            
            // Assembly points with detailed information
            assembly_points: [
                {
                    name: "Primary Assembly Point - Parking Lot",
                    capacity: "400 people",
                    distance: "100m from building",
                    coordinates: { lat: 11.848910, lon: 13.056651 },
                    safety_features: ["Open space", "Away from building", "Vehicle access for emergency services"],
                    route_from_emergency: getEvacuationRoute(locationInfo.floor, "parking_lot")
                },
                {
                    name: "Secondary Assembly Point - Front Courtyard",
                    capacity: "200 people", 
                    distance: "50m from building",
                    coordinates: { lat: 11.849110, lon: 13.056851 },
                    safety_features: ["Open space", "Near road access"],
                    route_from_emergency: getEvacuationRoute(locationInfo.floor, "courtyard")
                }
            ],
            
            // Emergency response information
            response_info: {
                severity: getSeverityLevel(emergencyType),
                priority: getPriorityLevel(emergencyType),
                estimated_response_time: getResponseTime(emergencyType),
                required_resources: getRequiredResources(emergencyType),
                immediate_actions: getImmediateActions(emergencyType)
            },
            
            // Environmental context
            environmental_context: {
                weather_conditions: "Clear, normal visibility",
                time_of_day: new Date().getHours() < 18 ? "Daytime" : "Evening",
                occupancy_estimate: Math.floor(Math.random() * 200) + 50, // Random occupancy 50-250
                visibility: "Good",
                temperature: "Normal room temperature",
                wind_conditions: "Calm"
            },
            
            // Detection information (simulating sensor data)
            detection_info: {
                detection_method: "Simulated Emergency",
                confidence_level: 1.0, // 100% confidence for simulation
                sensor_location: locationInfo.specific_location,
                detection_timestamp: new Date().toISOString(),
                verification_status: "Pending Gemini AI verification"
            },
            
            // Simulation metadata
            simulation: true,
            simulated_by: "Web App Emergency Simulation",
            simulation_timestamp: new Date().toISOString(),
            simulation_version: "2.0"
        };
        
        // Send to server
        const response = await fetch('/emergency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(emergencyData)
        });
        
        // Handle response with better error handling
        let responseData = null;
        try {
            responseData = await response.json();
        } catch (jsonError) {
            console.warn('Response is not JSON, treating as success for simulation');
            responseData = { status: 'success', message: 'Emergency processed' };
        }
        
        if (response.ok) {
            console.log(`✅ ${emergencyType} emergency simulation sent successfully`);
            console.log('Server response:', responseData);
            console.log('Emergency details:', emergencyData);
            
            // Show appropriate message based on response
            if (responseData && responseData.warning) {
                console.log(`⚠️ Simulation warning: ${responseData.warning}`);
            }
            
            // Show success feedback
            setTimeout(() => {
                buttons.forEach(btn => {
                    if (btn.textContent.includes('Sent') || btn.disabled) {
                        const icons = {
                            'Fire': 'fas fa-fire',
                            'Smoke': 'fas fa-smog',
                            'Accident': 'fas fa-car-crash',
                            'Fallen Person': 'fas fa-user-injured',
                            'Gun': 'fas fa-exclamation-circle',
                            'Blood': 'fas fa-tint'
                        };
                        btn.innerHTML = `<i class="${icons[emergencyType]}"></i><span>${emergencyType} Emergency</span>`;
                        btn.style.opacity = '1';
                        btn.disabled = false;
                    }
                });
            }, 2000);
            
            // Refresh alerts to show the new emergency
            if (window.alertAI) {
                setTimeout(() => {
                    window.alertAI.loadActiveAlerts();
                }, 1000);
            }
            
        } else {
            // Handle server errors but don't fail completely for simulations
            console.warn(`⚠️ Server returned ${response.status} for ${emergencyType} simulation`);
            console.warn('Response data:', responseData);
            
            // For simulations, we'll treat certain errors as warnings rather than failures
            if (response.status >= 400 && response.status < 600) {
                console.warn(`HTTP ${response.status} error, but simulation may have been processed`);
                
                // Show warning but still refresh alerts in case it worked
                setTimeout(() => {
                    buttons.forEach(btn => {
                        if (btn.disabled) {
                            const icons = {
                                'Fire': 'fas fa-fire',
                                'Smoke': 'fas fa-smog',
                                'Accident': 'fas fa-car-crash',
                                'Fallen Person': 'fas fa-user-injured',
                                'Gun': 'fas fa-exclamation-circle',
                                'Blood': 'fas fa-tint'
                            };
                            btn.innerHTML = `<i class="${icons[emergencyType]}"></i><span>${emergencyType} Emergency</span>`;
                            btn.style.opacity = '1';
                            btn.disabled = false;
                        }
                    });
                }, 2000);
                
                // Still try to refresh alerts
                if (window.alertAI) {
                    setTimeout(() => {
                        window.alertAI.loadActiveAlerts();
                    }, 1000);
                }
            } else {
                throw new Error(`Server responded with status: ${response.status} - ${responseData?.error || 'Unknown error'}`);
            }
        }
        
    } catch (error) {
        console.error(`❌ Error simulating ${emergencyType} emergency:`, error);
        
        // Show error feedback
        buttons.forEach(btn => {
            if (btn.disabled) {
                btn.innerHTML = `<i class="fas fa-exclamation-triangle"></i><span>Error - Try Again</span>`;
                btn.style.opacity = '1';
                btn.disabled = false;
                
                // Reset after 3 seconds
                setTimeout(() => {
                    const icons = {
                        'Fire': 'fas fa-fire',
                        'Smoke': 'fas fa-smog',
                        'Accident': 'fas fa-car-crash',
                        'Fallen Person': 'fas fa-user-injured',
                        'Gun': 'fas fa-exclamation-circle',
                        'Blood': 'fas fa-tint'
                    };
                    btn.innerHTML = `<i class="${icons[emergencyType]}"></i><span>${emergencyType} Emergency</span>`;
                }, 3000);
            }
        });
    }
}

// Helper functions for building data
function getFloorExtinguishers(floor) {
    const extinguishers = {
        'Ground Floor': [
            {"location": "Near main entrance", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
            {"location": "Kitchen area", "type": "Class K (Wet Chemical)", "capacity": "6 lbs", "last_inspection": "2024-01-15"},
            {"location": "Electrical room", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
        ],
        '1st Floor': [
            {"location": "Corridor near elevator", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
            {"location": "Emergency stairwell", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
            {"location": "Office area", "type": "CO2", "capacity": "10 lbs", "last_inspection": "2024-01-10"}
        ],
        '2nd Floor': [
            {"location": "Near conference room", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
            {"location": "Break room", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
            {"location": "Emergency exit", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
        ]
    };
    return extinguishers[floor] || [];
}

function getFloorExits(floor) {
    const exits = {
        'Ground Floor': [
            {"name": "Main entrance", "direction": "Front of building", "capacity": "200 people", "width": "Double doors"},
            {"name": "Back exit near parking", "direction": "Rear parking lot", "capacity": "150 people", "width": "Single door"}
        ],
        '1st Floor': [
            {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
            {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"}
        ],
        '2nd Floor': [
            {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
            {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"},
            {"name": "Fire escape", "direction": "North side", "capacity": "50 people", "width": "External ladder"}
        ]
    };
    return exits[floor] || [];
}

function getFloorHazards(floor) {
    const hazards = {
        'Ground Floor': ["High voltage electrical equipment in server room", "Natural gas lines in kitchen area", "Oxygen tanks in medical storage"],
        '1st Floor': ["Medical oxygen supply system", "Chemical storage room with flammables", "Server room with lithium batteries"],
        '2nd Floor': ["Backup generators with diesel fuel", "Propane tanks for heating system", "Chemical laboratory with various substances"]
    };
    return hazards[floor] || [];
}

function getSeverityLevel(emergencyType) {
    const severity = {
        'Fire': 'HIGH',
        'Smoke': 'HIGH', 
        'Gun': 'CRITICAL',
        'Blood': 'HIGH',
        'Fallen Person': 'MEDIUM',
        'Accident': 'MEDIUM'
    };
    return severity[emergencyType] || 'MEDIUM';
}

function getPriorityLevel(emergencyType) {
    const priority = {
        'Gun': 1,
        'Fire': 2,
        'Smoke': 2,
        'Blood': 3,
        'Fallen Person': 4,
        'Accident': 4
    };
    return priority[emergencyType] || 5;
}

function getResponseTime(emergencyType) {
    const responseTime = {
        'Gun': '2-3 minutes',
        'Fire': '3-5 minutes',
        'Smoke': '3-5 minutes', 
        'Blood': '4-6 minutes',
        'Fallen Person': '5-8 minutes',
        'Accident': '5-8 minutes'
    };
    return responseTime[emergencyType] || '5-10 minutes';
}

function getRequiredResources(emergencyType) {
    const resources = {
        'Fire': ['Fire department', 'Ambulance', 'Building security', 'Facility management'],
        'Smoke': ['Fire department', 'Building security', 'Facility management'],
        'Gun': ['Police', 'SWAT team', 'Ambulance', 'Building security'],
        'Blood': ['Ambulance', 'Medical team', 'Building security'],
        'Fallen Person': ['Ambulance', 'Medical team', 'Building security'],
        'Accident': ['Ambulance', 'Police', 'Building security']
    };
    return resources[emergencyType] || ['Emergency services', 'Building security'];
}

function getImmediateActions(emergencyType) {
    const actions = {
        'Fire': [
            'Activate fire alarm system',
            'Begin immediate evacuation',
            'Close fire doors',
            'Use nearest fire extinguisher if safe',
            'Proceed to assembly point'
        ],
        'Smoke': [
            'Activate fire alarm system',
            'Begin immediate evacuation',
            'Stay low to avoid smoke inhalation',
            'Use stairs, not elevators',
            'Proceed to assembly point'
        ],
        'Gun': [
            'Initiate lockdown procedures',
            'Run if safe to do so',
            'Hide if evacuation not possible',
            'Call 911 immediately',
            'Follow law enforcement instructions'
        ],
        'Blood': [
            'Secure the area',
            'Provide first aid if trained',
            'Apply pressure to bleeding wounds',
            'Call medical emergency services',
            'Keep victim conscious and calm'
        ],
        'Fallen Person': [
            'Check for consciousness and breathing',
            'Do not move unless in immediate danger',
            'Call medical emergency services',
            'Provide first aid if trained',
            'Keep victim warm and comfortable'
        ],
        'Accident': [
            'Secure the accident area',
            'Check for injuries',
            'Call emergency services',
            'Provide first aid if trained and safe',
            'Direct traffic away from area'
        ]
    };
    return actions[emergencyType] || ['Call emergency services', 'Secure the area', 'Provide assistance if safe'];
}

function getEvacuationRoute(floor, destination) {
    const routes = {
        'Ground Floor': {
            'parking_lot': ['Exit through main entrance', 'Turn left toward parking area', 'Proceed 100m to assembly point'],
            'courtyard': ['Exit through main entrance', 'Proceed straight to front courtyard', 'Gather at designated area']
        },
        '1st Floor': {
            'parking_lot': ['Use Emergency Stairwell A (East side)', 'Exit at ground level', 'Turn left toward parking area', 'Proceed 100m to assembly point'],
            'courtyard': ['Use Emergency Stairwell B (West side)', 'Exit at ground level', 'Proceed straight to front courtyard', 'Gather at designated area']
        },
        '2nd Floor': {
            'parking_lot': ['Use Emergency Stairwell A (East side)', 'Descend to ground level', 'Exit building', 'Turn left toward parking area', 'Proceed 100m to assembly point'],
            'courtyard': ['Use Emergency Stairwell B (West side)', 'Descend to ground level', 'Exit building', 'Proceed straight to front courtyard', 'Gather at designated area']
        }
    };
    return routes[floor] && routes[floor][destination] || ['Use nearest emergency exit', 'Proceed to designated assembly point'];
}

// Initialize the app
window.alertAI = new AlertAI();