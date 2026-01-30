// AlertAI Configuration
window.AlertAIConfig = {
    // Server URL - for combined server, use same domain
    serverUrl: window.location.origin, // Uses same domain as web app
    
    // For separate servers (legacy):
    // serverUrl: 'http://localhost:5000',
    
    // Other configuration options
    locationUpdateInterval: 30000, // 30 seconds
    alertCheckInterval: 30000,     // 30 seconds
    
    // Emergency types and their configurations
    emergencyTypes: {
        'Fire': {
            icon: 'fas fa-fire',
            agent: 'Fire Safety Agent',
            color: '#e74c3c'
        },
        'Smoke': {
            icon: 'fas fa-smog', 
            agent: 'Smoke Safety Agent',
            color: '#95a5a6'
        },
        'Fallen Person': {
            icon: 'fas fa-user-injured',
            agent: 'Medical Response Agent', 
            color: '#f39c12'
        },
        'Gun': {
            icon: 'fas fa-exclamation-circle',
            agent: 'Security Response Agent',
            color: '#8e44ad'
        },
        'Blood': {
            icon: 'fas fa-tint',
            agent: 'Trauma Response Agent',
            color: '#c0392b'
        }
    }
};