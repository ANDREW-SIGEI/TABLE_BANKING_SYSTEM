// Main application initialization
class TableBankingApp {
    constructor() {
        this.init();
    }

    init() {
        this.checkAuthentication();
        this.setupEventListeners();
    }

    checkAuthentication() {
        const token = localStorage.getItem('access_token');
        if (!token && !window.location.pathname.includes('login')) {
            window.location.href = '/login';
        }
    }

    setupEventListeners() {
        // Global event listeners
        console.log('Table Banking App initialized');
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    new TableBankingApp();
});
