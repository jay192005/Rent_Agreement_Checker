// script.js (Updated for Vercel Deployment)

document.addEventListener('DOMContentLoaded', () => {

    // --- Dynamic API Configuration ---
    // If running locally, use localhost. If on Vercel, use your deployed backend URL.
    const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
        ? 'http://127.0.0.1:5000'
        : 'https://your-deployed-backend-url.com'; // REPLACE THIS with your actual backend URL

    // --- Element Selections ---
    const getStartedNavBtn = document.getElementById('getStartedNavBtn');
    const userProfileIcon = document.getElementById('userProfileIcon');
    const authModal = document.getElementById('authModal');
    const closeBtn = document.querySelector('.close-btn');

    const openModalBtns = [
        document.getElementById('learnMoreBtn'),
        getStartedNavBtn
    ];

    const analyzeLeaseBtn = document.getElementById('analyzeLeaseBtn');
    const startFreeAnalysisBtn = document.getElementById('startFreeAnalysisBtn');

    const showSignup = document.getElementById('showSignup');
    const showLogin = document.getElementById('showLogin');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    // --- Core Functions ---

    function updateLoginState() {
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            if (getStartedNavBtn) getStartedNavBtn.classList.add('hidden');
            if (userProfileIcon) userProfileIcon.classList.remove('hidden');
        } else {
            if (getStartedNavBtn) getStartedNavBtn.classList.remove('hidden');
            if (userProfileIcon) userProfileIcon.classList.add('hidden');
        }
    }

    const handleFormSubmit = async (form, endpoint) => {
        const messageEl = form.querySelector('.form-message');
        const url = `${API_BASE_URL}${endpoint}`; // Combine base URL with the endpoint

        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                messageEl.textContent = result.message;
                messageEl.className = 'form-message success';

                if (result.email) {
                    localStorage.setItem('userEmail', result.email);
                    updateLoginState();
                }

                form.reset();
                setTimeout(closeModal, 1500);
            } else {
                messageEl.textContent = result.error || 'An error occurred.';
                messageEl.className = 'form-message error';
            }
        } catch (error) {
            console.error("Fetch error:", error);
            messageEl.textContent = 'Could not connect to the server.';
            messageEl.className = 'form-message error';
        }
    };

    function logout() {
        localStorage.removeItem('userEmail');
        updateLoginState();
    }

    function goToAnalyzer() {
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            window.location.href = 'analyzer.html';
        } else {
            openModal();
        }
    }

    // --- Modal Logic ---
    const openModal = () => { authModal.style.display = 'flex'; };
    const closeModal = () => { authModal.style.display = 'none'; };

    // --- Event Listeners ---
    openModalBtns.forEach(btn => {
        if(btn) btn.addEventListener('click', openModal);
    });

    if(closeBtn) closeBtn.addEventListener('click', closeModal);
    
    window.addEventListener('click', (e) => {
        if (e.target === authModal) closeModal();
    });

    if(analyzeLeaseBtn) analyzeLeaseBtn.addEventListener('click', goToAnalyzer);
    if(startFreeAnalysisBtn) startFreeAnalysisBtn.addEventListener('click', goToAnalyzer);

    if(showSignup) {
        showSignup.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.style.display = 'none';
            signupForm.style.display = 'block';
        });
    }

    if(showLogin) {
        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            signupForm.style.display = 'none';
            loginForm.style.display = 'block';
        });
    }

    if(signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(signupForm, '/api/register'); // Use relative endpoint
        });
    }

    if(loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(loginForm, '/api/login'); // Use relative endpoint
        });
    }

    if(userProfileIcon) userProfileIcon.addEventListener('click', logout);

    updateLoginState();
});
