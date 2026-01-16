// history.js

document.addEventListener('DOMContentLoaded', () => {
    const historyListContainer = document.getElementById('history-list-container');
    const loadingView = document.getElementById('loading-history');
    const noHistoryView = document.getElementById('no-history');

    /**
     * Checks if user is logged in. If not, redirects to the home page.
     */
    function checkAuthentication() {
        const userEmail = localStorage.getItem('userEmail');
        if (!userEmail) {
            // User shouldn't be here without being logged in
            window.location.href = 'index.html';
        }
        return userEmail;
    }

    /**
     * Fetches and displays the analysis history for the logged-in user.
     */
    async function fetchAndDisplayHistory(email) {
        loadingView.classList.remove('hidden');
        historyListContainer.innerHTML = ''; // Clear previous content

        try {
            const response = await fetch(`http://localhost:5000/api/history/${email}`);
            if (!response.ok) {
                throw new Error('Failed to fetch history.');
            }

            const historyData = await response.json();

            if (historyData.length === 0) {
                noHistoryView.classList.remove('hidden');
            } else {
                historyData.forEach(item => {
                    // The backend now sends a parsed JSON object directly. No need to parse again.
                    const result = item.analysis_result;
                    
                    const historyItemEl = document.createElement('div');
                    historyItemEl.className = 'history-item';

                    // Format the date for better readability
                    const analysisDate = new Date(item.created_at).toLocaleString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    });

                    historyItemEl.innerHTML = `
                        <div class="history-item-header">
                            <h3>${result.ratingText} - Score: ${result.ratingScore}/100</h3>
                            <span class="history-item-date">${analysisDate}</span>
                        </div>
                        <div class="history-item-summary">
                            <p><strong>Summary:</strong> ${result.shortSummary}</p>
                            <div class="clause-counts" style="padding-top: 10px; border-top: none; margin-top: 10px;">
                                <div class="clause-count red">Red Flags: ${result.redFlagsCount}</div>
                                <div class="clause-count green">Fair Clauses: ${result.fairClausesCount}</div>
                            </div>
                        </div>
                    `;
                    historyListContainer.appendChild(historyItemEl);
                });
            }

        } catch (error) {
            console.error("Error fetching history:", error);
            historyListContainer.innerHTML = `<p style="color: red; text-align: center;">Could not load your history. Please try again later.</p>`;
        } finally {
            loadingView.classList.add('hidden');
        }
    }

    // --- Initial Page Load ---
    const userEmail = checkAuthentication();
    if (userEmail) {
        fetchAndDisplayHistory(userEmail);
    }
});