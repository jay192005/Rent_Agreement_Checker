// analyzer.js - Logic for the document analysis page (Updated)

document.addEventListener('DOMContentLoaded', () => {

    // --- Element Selections ---
    const stateLocation = document.getElementById('state-location');
    const uploadTab = document.getElementById('upload-tab');
    const pasteTab = document.getElementById('paste-tab');
    const uploadView = document.getElementById('upload-view');
    const pasteView = document.getElementById('paste-view');
    const dropZone = document.getElementById('drop-zone');
    const fileUpload = document.getElementById('file-upload');
    const chooseFileBtn = document.getElementById('choose-file-btn');
    const pasteTextArea = document.getElementById('paste-text-area');
    const charCount = document.getElementById('char-count');
    const analyzeBtn = document.getElementById('analyze-btn');

    // View containers
    const formSection = document.getElementById('analyzer-form-section');
    const loadingView = document.getElementById('loading-view');
    const resultsView = document.getElementById('results-view');

    // Results elements
    const resultRatingText = document.getElementById('result-rating-text');
    const resultRatingScore = document.getElementById('result-rating-score');
    const resultShortSummary = document.getElementById('result-short-summary');
    const redFlagsCount = document.getElementById('red-flags-count');
    const fairClausesCount = document.getElementById('fair-clauses-count');
    const dangerMarker = document.getElementById('danger-marker');
    const aiSummaryText = document.getElementById('ai-summary-text');
    const redFlagsTabCount = document.getElementById('red-flags-tab-count');
    const fairClausesTabCount = document.getElementById('fair-clauses-tab-count');
    const redFlagsContent = document.getElementById('red-flags');
    const fairClausesContent = document.getElementById('fair-clauses');
    const recommendationsList = document.getElementById('recommendations-list');
    const resultsTabs = document.querySelectorAll('.results-tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    let selectedFile = null;
    let pasteContent = '';

    // --- Core Functions ---

    /**
     * Populates the state dropdown with Indian states and territories.
     */
    function populateIndianStates() {
        const indianStates = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
            "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
            "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
            "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
            "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
            "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
        ];

        if (stateLocation) {
            indianStates.sort().forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateLocation.appendChild(option);
            });
        }
    }

    /**
     * Checks if user is logged in. If not, redirects to the home page.
     */
    function checkAuthentication() {
        const userEmail = localStorage.getItem('userEmail');
        if (!userEmail) {
            // If user is not logged in, they can't be here. Redirect them.
            window.location.href = 'index.html';
        }
    }
    
    /**
     * Updates the state of the analyze button based on input.
     */
    function updateAnalyzeButtonState() {
        if (selectedFile || pasteContent.length > 0) {
            analyzeBtn.disabled = false;
        } else {
            analyzeBtn.disabled = true;
        }
    }

    /**
     * Handles file selection and updates the UI.
     */
    function handleFileSelect(file) {
        if (!file) return;
        selectedFile = file;
        pasteContent = ''; // Clear paste content if a file is selected
        if (dropZone) {
            const prompt = dropZone.querySelector('.drop-zone-prompt');
            prompt.innerHTML = `<p><strong>File Selected:</strong> ${file.name}</p>`;
        }
        updateAnalyzeButtonState();
    }

    /**
     * Handles the analysis by sending data to the backend API.
     */
    async function handleAnalysis() {
        if (!selectedFile && pasteContent.length === 0) return;

        formSection.classList.add('hidden');
        loadingView.classList.remove('hidden');

        const formData = new FormData();
        if (selectedFile) {
            formData.append('file', selectedFile);
        } else {
            formData.append('text', pasteContent);
        }
        formData.append('state', stateLocation.value);

        // --- ⭐️ KEY UPDATE: Add user's email to the request ---
        // This tells the backend who is making the request so the result can be saved to their history.
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            formData.append('email', userEmail);
        }
        // --- End of Update ---

        try {
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Analysis failed');
            }

            const result = await response.json();
            displayResults(result);

        } catch (error) {
            console.error('Analysis Error:', error);
            loadingView.classList.add('hidden');
            formSection.classList.remove('hidden');
            alert(`An error occurred: ${error.message}`);
        }
    }
    
    /**
     * Populates the results view with data from the analysis.
     */
    function displayResults(data) {
        resultRatingText.textContent = data.ratingText;
        resultRatingScore.textContent = `${data.ratingScore}/100`;
        resultShortSummary.textContent = data.shortSummary;
        redFlagsCount.textContent = `Red Flags: ${data.redFlagsCount}`;
        fairClausesCount.textContent = `Fair Clauses: ${data.fairClausesCount}`;
        
        dangerMarker.style.left = `${data.ratingScore}%`;
        aiSummaryText.textContent = data.aiSummary;

        redFlagsTabCount.textContent = data.redFlagsCount;
        fairClausesTabCount.textContent = data.fairClausesCount;

        // Populate Red Flags
        redFlagsContent.innerHTML = '';
        if (data.redFlags && data.redFlags.length > 0) {
            data.redFlags.forEach(item => {
                const clauseEl = document.createElement('div');
                clauseEl.className = 'clause-item';
                clauseEl.innerHTML = `
                    <div class="clause-priority ${item.priority.toLowerCase()}"><span>${item.priority.toUpperCase()} Priority</span></div>
                    <h4>${item.title}</h4>
                    <p><strong>Issue Identified:</strong> ${item.issue}</p>
                    <p><strong>AI Recommendation:</strong> ${item.recommendation}</p>
                `;
                redFlagsContent.appendChild(clauseEl);
            });
        } else {
            redFlagsContent.innerHTML = '<p>No significant red flags were found in this document. Good job!</p>';
        }

        // Populate Fair Clauses
        fairClausesContent.innerHTML = '';
        if (data.fairClauses && data.fairClauses.length > 0) {
            data.fairClauses.forEach(item => {
                const clauseEl = document.createElement('div');
                clauseEl.className = 'clause-item fair';
                clauseEl.innerHTML = `
                    <h4>${item.title}</h4>
                    <p>${item.recommendation}</p>
                `;
                fairClausesContent.appendChild(clauseEl);
            });
        } else {
            fairClausesContent.innerHTML = '<p>No specifically fair or positive clauses were highlighted by the AI.</p>';
        }


        // Populate Recommendations
        recommendationsList.innerHTML = '';
         if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                recommendationsList.appendChild(li);
            });
        } else {
            recommendationsList.innerHTML = '<li>No specific next steps were provided. Review the identified clauses carefully.</li>';
        }


        loadingView.classList.add('hidden');
        resultsView.classList.remove('hidden');
    }


    // --- Event Listeners ---
    
    if(uploadTab) {
        uploadTab.addEventListener('click', () => {
            uploadTab.classList.add('active');
            pasteTab.classList.remove('active');
            uploadView.classList.remove('hidden');
            pasteView.classList.add('hidden');
        });
    }

    if(pasteTab) {
        pasteTab.addEventListener('click', () => {
            pasteTab.classList.add('active');
            uploadTab.classList.remove('active');
            pasteView.classList.remove('hidden');
            uploadView.classList.add('hidden');
        });
    }

    if (dropZone) {
        dropZone.addEventListener('click', () => fileUpload.click());
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, e => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });
        dropZone.addEventListener('drop', e => handleFileSelect(e.dataTransfer.files[0]), false);
    }
    
    if (chooseFileBtn) chooseFileBtn.addEventListener('click', () => fileUpload.click());
    if (fileUpload) fileUpload.addEventListener('change', e => handleFileSelect(e.target.files[0]));

    if (pasteTextArea) {
        pasteTextArea.addEventListener('input', () => {
            pasteContent = pasteTextArea.value;
            selectedFile = null;
            if(dropZone){
                 const prompt = dropZone.querySelector('.drop-zone-prompt');
                 prompt.innerHTML = `<p><strong>Drag & drop your lease document here</strong></p><p class="small-text">or click to browse your files</p>`;
            }
            charCount.textContent = `${pasteContent.length} characters`;
            updateAnalyzeButtonState();
        });
    }

    if(analyzeBtn) analyzeBtn.addEventListener('click', handleAnalysis);

    if(resultsTabs) {
        resultsTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                resultsTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                tabContents.forEach(content => content.classList.remove('active'));
                const activeTabContent = document.getElementById(tab.dataset.tab);
                if(activeTabContent) {
                    activeTabContent.classList.add('active');
                }
            });
        });
    }

    // --- Initial Page Load ---
    checkAuthentication();
    populateIndianStates();
});