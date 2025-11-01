class Dashboard {
    async init() {
        await this.loadStats();
    }

    async loadStats() {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('/api/dashboard/stats/', {
                headers: {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                document.getElementById('totalGroups').textContent = data.total_groups;
                document.getElementById('totalMembers').textContent = data.total_members;
                document.getElementById('activeLoans').textContent = data.active_loans;
                document.getElementById('totalSavings').textContent = 'KES ' + data.total_savings.toLocaleString();
            } else {
                console.error('Failed to load stats');
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard().init();
});

function showPage(page) {
    alert('Navigating to: ' + page);
    // Implementation for page navigation
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login/';
}
