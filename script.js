// script.js (Complete updated version for the landing page with multi-page navigation)

document.addEventListener('DOMContentLoaded', () => {

    // --- Element Selections ---
    const getStartedNavBtn = document.getElementById('getStartedNavBtn');
    const userProfileIcon = document.getElementById('userProfileIcon');
    const authModal = document.getElementById('authModal');
    const closeBtn = document.querySelector('.close-btn');

    // Buttons that open the login modal
    const openModalBtns = [
        document.getElementById('learnMoreBtn'), // The "Learn More" button in the hero section
        getStartedNavBtn // The "Log In" button in the nav
    ];

    // Buttons that navigate to the analyzer page
    const analyzeLeaseBtn = document.getElementById('analyzeLeaseBtn');
    const startFreeAnalysisBtn = document.getElementById('startFreeAnalysisBtn');

    // Form-related elements
    const showSignup = document.getElementById('showSignup');
    const showLogin = document.getElementById('showLogin');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    // --- Core Functions ---

    /**
     * Checks localStorage to see if a user is logged in and updates the nav bar.
     */
    function updateLoginState() {
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            // User is logged in: Show icon, hide button
            getStartedNavBtn.classList.add('hidden');
            userProfileIcon.classList.remove('hidden');
        } else {
            // User is logged out: Hide icon, show button
            getStartedNavBtn.classList.remove('hidden');
            userProfileIcon.classList.add('hidden');
        }
    }

    /**
     * Handles the login/signup form submission.
     */
    const handleFormSubmit = async (form, url) => {
        const messageEl = form.querySelector('.form-message');
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
            messageEl.textContent = 'Could not connect to the server.';
            messageEl.className = 'form-message error';
        }
    };

    /**
     * Logs the user out.
     */
    function logout() {
        localStorage.removeItem('userEmail');
        updateLoginState();
    }

    /**
     * Navigates to the analyzer page or opens the login modal if the user is not authenticated.
     */
    function goToAnalyzer() {
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            // If logged in, navigate to the new analyzer page
            window.location.href = 'analyzer.html';
        } else {
            // If not logged in, open the login modal to prompt them
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

    // Event listeners for the main "Analyze" buttons
    if(analyzeLeaseBtn) analyzeLeaseBtn.addEventListener('click', goToAnalyzer);
    if(startFreeAnalysisBtn) startFreeAnalysisBtn.addEventListener('click', goToAnalyzer);

    // Event listeners for switching between login/signup forms
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

    // Event listeners for form submissions
    if(signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(signupForm, 'http://localhost:5000/api/register');
        });
    }

    if(loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(loginForm, 'http://localhost:5000/api/login');
        });
    }

    // Event listener for logout
    if(userProfileIcon) userProfileIcon.addEventListener('click', logout);

    // --- Initial Page Load ---
    // Set the correct UI state as soon as the page loads
    updateLoginState();
});

