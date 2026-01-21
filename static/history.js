// history.js - Logic for the analysis history page

document.addEventListener('DOMContentLoaded', () => {

    // --- Element Selections ---
    const loadingView = document.getElementById('loading-view');
    const historyListContainer = document.getElementById('history-list');
    const noHistoryMessage = document.getElementById('no-history-message');
    const backToAnalyzerBtn = document.getElementById('back-to-analyzer-btn');

    // --- Core Functions ---

    /**
     * Checks if user is logged in and returns their email.
     * If not logged in, redirects to home page.
     */
    function checkAuthentication() {
        const userEmail = localStorage.getItem('userEmail');
        if (!userEmail) {
            window.location.href = 'index.html';
            return null;
        }
        return userEmail;
    }

    /**
     * Fetches and displays the analysis history for the logged-in user.
     */
    async function fetchAndDisplayHistory(email) {
        if (!email) return;

        if (loadingView) loadingView.classList.remove('hidden');
        if (historyListContainer) historyListContainer.innerHTML = ''; // Clear previous content

        try {
            const response = await fetch(`/api/history/${encodeURIComponent(email)}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const history = await response.json();

            if (loadingView) loadingView.classList.add('hidden');

            if (history.length === 0) {
                // No history found
                if (noHistoryMessage) noHistoryMessage.classList.remove('hidden');
                if (historyListContainer) historyListContainer.classList.add('hidden');
            } else {
                // Display history
                if (noHistoryMessage) noHistoryMessage.classList.add('hidden');
                if (historyListContainer) historyListContainer.classList.remove('hidden');
                
                displayHistoryItems(history);
            }

        } catch (error) {
            console.error("Error fetching history:", error);
            
            if (loadingView) loadingView.classList.add('hidden');
            
            if (historyListContainer) {
                historyListContainer.innerHTML = `
                    <div class="error-message">
                        <p style="color: red; text-align: center;">
                            Could not load your history. Please try again later.
                        </p>
                        <p style="text-align: center;">
                            <button onclick="location.reload()" class="btn btn-secondary">
                                Retry
                            </button>
                        </p>
                    </div>
                `;
                historyListContainer.classList.remove('hidden');
            }
        }
    }

    /**
     * Displays the history items in the UI.
     */
    function displayHistoryItems(history) {
        if (!historyListContainer) return;

        historyListContainer.innerHTML = '';

        history.forEach((item, index) => {
            const analysisData = item.analysis_result;
            const createdDate = new Date(item.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            // Determine rating class for styling
            let ratingClass = 'safe';
            if (analysisData.ratingScore < 30) ratingClass = 'critical';
            else if (analysisData.ratingScore < 50) ratingClass = 'danger';
            else if (analysisData.ratingScore < 70) ratingClass = 'caution';

            historyItem.innerHTML = `
                <div class="history-item-header">
                    <div class="history-item-title">
                        <h3>Analysis #${history.length - index}</h3>
                        <span class="history-item-date">${createdDate}</span>
                    </div>
                    <div class="history-item-rating ${ratingClass}">
                        <span class="rating-score">${analysisData.ratingScore}/100</span>
                        <span class="rating-text">${analysisData.ratingText}</span>
                    </div>
                </div>
                
                <div class="history-item-summary">
                    <p>${analysisData.shortSummary}</p>
                </div>
                
                <div class="history-item-stats">
                    <div class="stat">
                        <span class="stat-number">${analysisData.redFlagsCount || 0}</span>
                        <span class="stat-label">Red Flags</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">${analysisData.fairClausesCount || 0}</span>
                        <span class="stat-label">Fair Clauses</span>
                    </div>
                </div>
                
                <div class="history-item-actions">
                    <button class="btn btn-secondary view-details-btn" data-index="${index}">
                        View Details
                    </button>
                </div>
                
                <div class="history-item-details" id="details-${index}" style="display: none;">
                    <div class="details-section">
                        <h4>AI Summary</h4>
                        <p>${analysisData.aiSummary}</p>
                    </div>
                    
                    ${analysisData.redFlags && analysisData.redFlags.length > 0 ? `
                        <div class="details-section">
                            <h4>Red Flags (${analysisData.redFlags.length})</h4>
                            ${analysisData.redFlags.map(flag => `
                                <div class="flag-item">
                                    <div class="flag-priority ${flag.priority.toLowerCase()}">${flag.priority.toUpperCase()}</div>
                                    <h5>${flag.title}</h5>
                                    <p><strong>Issue:</strong> ${flag.issue}</p>
                                    <p><strong>Recommendation:</strong> ${flag.recommendation}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${analysisData.fairClauses && analysisData.fairClauses.length > 0 ? `
                        <div class="details-section">
                            <h4>Fair Clauses (${analysisData.fairClauses.length})</h4>
                            ${analysisData.fairClauses.map(clause => `
                                <div class="clause-item">
                                    <h5>${clause.title}</h5>
                                    <p>${clause.recommendation}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${analysisData.recommendations && analysisData.recommendations.length > 0 ? `
                        <div class="details-section">
                            <h4>Recommendations</h4>
                            <ul>
                                ${analysisData.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;

            historyListContainer.appendChild(historyItem);
        });

        // Add event listeners for view details buttons
        const viewDetailsBtns = historyListContainer.querySelectorAll('.view-details-btn');
        viewDetailsBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = e.target.dataset.index;
                const detailsDiv = document.getElementById(`details-${index}`);
                
                if (detailsDiv.style.display === 'none') {
                    detailsDiv.style.display = 'block';
                    btn.textContent = 'Hide Details';
                } else {
                    detailsDiv.style.display = 'none';
                    btn.textContent = 'View Details';
                }
            });
        });
    }

    // --- Event Listeners ---
    
    if (backToAnalyzerBtn) {
        backToAnalyzerBtn.addEventListener('click', () => {
            window.location.href = 'analyzer.html';
        });
    }

    // --- Initial Page Load ---
    const userEmail = checkAuthentication();
    if (userEmail) {
        fetchAndDisplayHistory(userEmail);
    }
    
    // Add user profile icon functionality
    const userProfileIcon = document.getElementById('userProfileIcon');
    if (userProfileIcon) {
        userProfileIcon.addEventListener('click', () => {
            const userEmail = localStorage.getItem('userEmail');
            if (userEmail) {
                if (confirm(`Logged in as: ${userEmail}\n\nDo you want to log out?`)) {
                    localStorage.removeItem('userEmail');
                    window.location.href = 'index.html';
                }
            } else {
                window.location.href = 'index.html';
            }
        });
    }
});