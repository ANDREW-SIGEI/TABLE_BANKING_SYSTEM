class Dashboard {
    async init() {
        await this.loadStats();
    }

    async loadStats() {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch('/api/method/tablebanking.api.dashboard_api.get_dashboard_stats', {
                headers: {'Authorization': 'Bearer ' + token}
            });
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('totalGroups').textContent = data.stats.total_groups;
                document.getElementById('totalMembers').textContent = data.stats.total_members;
                document.getElementById('activeLoans').textContent = data.stats.active_loans;
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard().init();
});

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}
